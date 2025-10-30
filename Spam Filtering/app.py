import joblib
from flask import Flask, request, jsonify

# 1. Initialize the Flask app
app = Flask(__name__)

# 2. Load your saved model and vectorizer
#    These files must be in the same folder as app.py
try:
    model = joblib.load('model.joblib')
    vectorizer = joblib.load('vectorizer.joblib')
    print("Model and vectorizer loaded successfully")
except FileNotFoundError:
    print("Error: model.joblib or vectorizer.joblib not found.")
    model = None
    vectorizer = None

# 3. Define a prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if not model or not vectorizer:
        return jsonify({'error': 'Model is not loaded'}), 500

    try:
        # Get the JSON data from the request
        data = request.get_json()
        message = data['message']

        # The vectorizer expects a list
        new_message_tfidf = vectorizer.transform([message])
        
        # Make the prediction
        prediction = model.predict(new_message_tfidf)
        
        # Convert the prediction (which is a numpy int) to a standard Python int
        prediction_int = int(prediction[0])
        label = 'Spam' if prediction_int == 1 else 'Ham'

        # Return the result as JSON
        return jsonify({
            'prediction': prediction_int,
            'label': label,
            'message': message
        })
        
    except KeyError:
        # If the 'message' key is missing from the JSON
        return jsonify({'error': "Missing 'message' key in request JSON"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# This makes the app runnable from the command line
if __name__ == '__main__':
    app.run(debug=True, port=5000)