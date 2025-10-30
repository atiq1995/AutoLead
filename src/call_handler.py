"""
AUTOLEADAI - Main Call Handler
Orchestrates the complete call processing pipeline
Author: Team AUTOLEADAI
"""
import logging
from pathlib import Path
from typing import Dict
from datetime import datetime
import config

from src.audio_processor import AudioProcessor
from src.speech_to_text import get_stt_engine
from src.spam_detector import get_spam_detector
from src.call_logger import get_call_logger

# Setup logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)


class CallHandler:
    """
    Main orchestrator for call processing pipeline
    Coordinates audio processing, transcription, spam detection, and logging
    """
    
    def __init__(self):
        """Initialize call handler and all components"""
        logger.info("Initializing CallHandler...")
        
        self.audio_processor = AudioProcessor()
        self.stt_engine = get_stt_engine()
        self.spam_detector = get_spam_detector()
        self.call_logger = get_call_logger()
        
        logger.info("CallHandler initialized successfully")
    
    def process_call(self, audio_source: str, source_type: str = 'file') -> Dict:
        """
        Process a complete call through the pipeline
        
        Args:
            audio_source: Path to audio file or duration for recording
            source_type: 'file' for existing file, 'record' for new recording
        
        Returns:
            Dictionary with complete processing results
        """
        try:
            start_time = datetime.now()
            logger.info(f"Starting call processing: {audio_source} ({source_type})")
            
            # Step 1: Get/Record Audio
            if source_type == 'record':
                duration = int(audio_source)
                audio_path = self.audio_processor.record_audio(duration)
            elif source_type == 'file':
                audio_path = self.audio_processor.load_audio_file(audio_source)
            else:
                raise ValueError(f"Invalid source_type: {source_type}")
            
            logger.info(f"Audio acquired: {audio_path}")
            
            # Step 2: Audio Preprocessing (Noise Reduction)
            processed_audio = self.audio_processor.process_audio(audio_path)
            logger.info("Audio preprocessing completed")
            
            # Step 3: Speech-to-Text Conversion
            transcript = self.stt_engine.transcribe(processed_audio)
            
            if not transcript.get('success'):
                logger.error("Transcription failed")
                return {
                    'success': False,
                    'error': 'Transcription failed',
                    'audio_path': audio_path
                }
            
            logger.info(f"Transcription completed: {len(transcript['text'])} characters")
            
            # Step 4: Spam Detection
            spam_result = self.spam_detector.predict(transcript['text'])
            spam_features = self.spam_detector.analyze_features(transcript['text'])
            spam_result['features'] = spam_features
            
            logger.info(f"Spam detection: {'SPAM' if spam_result['is_spam'] else 'LEGITIMATE'}")
            
            # Step 5: Calculate Duration
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Step 6: Log to Database
            call_id = self.call_logger.log_call(
                audio_path=processed_audio,
                transcript=transcript,
                spam_result=spam_result,
                duration=processing_time,
                metadata={
                    'source_type': source_type,
                    'processing_time': processing_time,
                    'original_audio': audio_path
                }
            )
            
            logger.info(f"Call logged: call_id={call_id}")
            
            # Step 7: Handle Spam
            if spam_result['is_spam']:
                self._handle_spam_call(call_id, processed_audio, transcript, spam_result)
            
            # Prepare result
            result = {
                'success': True,
                'call_id': call_id,
                'audio_path': processed_audio,
                'transcript': transcript['text'],
                'is_spam': spam_result['is_spam'],
                'spam_confidence': spam_result['confidence'],
                'spam_features': spam_features,
                'processing_time': processing_time,
                'status': 'spam_blocked' if spam_result['is_spam'] else 'processed'
            }
            
            logger.info(f"Call processing completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Call processing failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _handle_spam_call(self, call_id: int, audio_path: str, 
                         transcript: Dict, spam_result: Dict):
        """
        Handle detected spam call
        
        Args:
            call_id: Database call ID
            audio_path: Path to audio file
            transcript: Transcript data
            spam_result: Spam detection result
        """
        try:
            # Move audio to spam directory
            spam_dir = Path(config.SPAM_STORAGE_PATH)
            spam_dir.mkdir(parents=True, exist_ok=True)
            
            # Create spam log file
            spam_log_path = spam_dir / f"spam_call_{call_id}.txt"
            with open(spam_log_path, 'w', encoding='utf-8') as f:
                f.write(f"SPAM CALL DETECTED\n")
                f.write(f"=" * 50 + "\n")
                f.write(f"Call ID: {call_id}\n")
                f.write(f"Audio: {audio_path}\n")
                f.write(f"Confidence: {spam_result['confidence']:.2%}\n")
                f.write(f"\nTranscript:\n{transcript['text']}\n")
                f.write(f"\nSpam Features:\n")
                for category, data in spam_result.get('features', {}).items():
                    f.write(f"  {category}: {data}\n")
            
            logger.info(f"Spam call handled: {spam_log_path}")
            
        except Exception as e:
            logger.error(f"Failed to handle spam call: {e}")
    
    def get_call_statistics(self) -> Dict:
        """Get processing statistics"""
        return self.call_logger.get_statistics()
    
    def get_recent_calls(self, limit: int = 10) -> list:
        """Get recent calls"""
        return self.call_logger.get_all_calls(limit=limit)

