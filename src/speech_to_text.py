"""
AUTOLEADAI - Speech to Text Module
Handles real-time speech recognition using OpenAI Whisper
Author: Awais Ahmad

TODO: Add support for multiple languages
TODO: Implement streaming transcription for real-time calls
TODO: Optimize model loading time (currently takes 2-3 seconds)
"""
import whisper
import torch
import logging
import os
from pathlib import Path
from typing import Optional, Dict
import config

# Setup logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Set ffmpeg path for Whisper
try:
    import imageio_ffmpeg
    os.environ["PATH"] = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe()) + os.pathsep + os.environ.get("PATH", "")
    logger.info(f"Using ffmpeg from: {imageio_ffmpeg.get_ffmpeg_exe()}")
except ImportError:
    logger.warning("imageio-ffmpeg not found, Whisper may not work without system ffmpeg")


class SpeechToText:
    """
    Speech-to-text conversion using OpenAI Whisper model
    Provides accurate transcription with minimal latency
    """
    
    def __init__(self, model_size: str = config.WHISPER_MODEL):
        """
        Initialize the Whisper model
        
        Args:
            model_size: Size of Whisper model (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing Whisper model on {self.device}")
        self._load_model()
    
    def _load_model(self):
        """Load the Whisper model into memory"""
        try:
            logger.info(f"Loading Whisper {self.model_size} model...")
            self.model = whisper.load_model(self.model_size, device=self.device)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def transcribe(self, audio_path: str, language: str = config.WHISPER_LANGUAGE) -> Dict:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            language: Language code (default: 'en')
        
        Returns:
            Dictionary containing transcript and metadata
        """
        try:
            logger.info(f"Transcribing audio: {audio_path}")
            
            # Convert path to absolute
            audio_path = os.path.abspath(audio_path)
            logger.info(f"Absolute path: {audio_path}")
            
            # Check if file exists
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
            # Load audio using librosa (doesn't need ffmpeg)
            # Note: Initially tried Whisper's built-in audio loading but had ffmpeg issues on Windows
            # This approach using librosa works better - discussed with team on Oct 20
            import librosa
            import numpy as np
            
            logger.info("Loading audio with librosa...")
            audio_data, sr = librosa.load(audio_path, sr=16000, mono=True)
            
            # Ensure audio is in correct format for Whisper
            audio_data = audio_data.astype(np.float32)
            logger.info(f"Audio loaded: {len(audio_data)} samples at {sr}Hz")
            
            # Perform transcription with audio array instead of file path
            result = self.model.transcribe(
                audio_data,
                language=language,
                fp16=False,  # Use FP32 for CPU compatibility
                verbose=False
            )
            
            transcript_data = {
                'text': result['text'].strip(),
                'language': result['language'],
                'segments': result['segments'],
                'success': True,
                'audio_path': audio_path
            }
            
            logger.info(f"Transcription successful: {len(transcript_data['text'])} characters")
            return transcript_data
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                'text': '',
                'success': False,
                'error': str(e),
                'audio_path': audio_path
            }
    
    def transcribe_realtime(self, audio_chunk: bytes) -> str:
        """
        Transcribe audio chunk in real-time
        
        Args:
            audio_chunk: Raw audio bytes
        
        Returns:
            Transcribed text
        """
        # This would be used for streaming audio in production
        # For demo, we'll use file-based transcription
        pass


# Singleton instance
_stt_instance: Optional[SpeechToText] = None


def get_stt_engine() -> SpeechToText:
    """Get or create singleton instance of SpeechToText"""
    global _stt_instance
    if _stt_instance is None:
        _stt_instance = SpeechToText()
    return _stt_instance

