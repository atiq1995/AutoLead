"""
AUTOLEADAI - Demo Web Interface
Flask web application for demonstrating Module 1
Author: Team AUTOLEADAI
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from pathlib import Path
from src.call_handler import CallHandler
import config

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Call Handler
call_handler = CallHandler()

# Upload folder
UPLOAD_FOLDER = 'uploads'
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size


@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('index.html')


@app.route('/api/process-call', methods=['POST'])
def process_call():
    """
    Process a call from uploaded audio file
    """
    try:
        # Check if file was uploaded
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No audio file provided'
            }), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Save uploaded file
        filename = f"upload_{Path(file.filename).stem}_{os.urandom(4).hex()}.wav"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"Processing uploaded file: {filepath}")
        
        # Process the call
        result = call_handler.process_call(filepath, source_type='file')
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing call: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/record-call', methods=['POST'])
def record_call():
    """
    Record and process a new call
    """
    try:
        data = request.get_json()
        duration = data.get('duration', 10)  # Default 10 seconds
        
        logger.info(f"Recording call for {duration} seconds")
        
        # Process recorded call
        result = call_handler.process_call(str(duration), source_type='record')
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error recording call: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get call processing statistics"""
    try:
        stats = call_handler.get_call_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/recent-calls', methods=['GET'])
def get_recent_calls():
    """Get recent processed calls"""
    try:
        limit = request.args.get('limit', 10, type=int)
        calls = call_handler.get_recent_calls(limit=limit)
        
        return jsonify({
            'success': True,
            'calls': calls
        })
    except Exception as e:
        logger.error(f"Error getting recent calls: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'module': 'Module 1: Call Handling and Speech Processing',
        'version': '1.0.0'
    })


if __name__ == '__main__':
    logger.info("Starting AUTOLEADAI Module 1 Demo Server...")
    logger.info("Access the dashboard at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

