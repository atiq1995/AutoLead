"""
AUTOLEADAI - Audio Processing Module
Handles audio recording, noise reduction, and preprocessing
Author: Aima Asghar & Awais Ahmad

TODO: Add automatic gain control
TODO: Improve noise reduction - currently too aggressive on some files
TODO: Support for batch processing multiple files
"""
import pyaudio
import wave
import noisereduce as nr
import librosa
import soundfile as sf
import numpy as np
import logging
from pathlib import Path
from datetime import datetime
import config

# Setup logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)


class AudioProcessor:
    """
    Handles audio capture, recording, and preprocessing
    Includes noise reduction and audio enhancement
    """
    
    def __init__(self):
        """Initialize audio processor"""
        self.sample_rate = config.SAMPLE_RATE
        self.channels = config.CHANNELS
        self.chunk_size = 1024
        self.audio = None
        self.stream = None
        
    def record_audio(self, duration: int, output_path: str = None) -> str:
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds
            output_path: Path to save the recording
        
        Returns:
            Path to saved audio file
        """
        try:
            # Initialize PyAudio
            self.audio = pyaudio.PyAudio()
            
            logger.info(f"Starting audio recording for {duration} seconds...")
            
            # Open stream
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            frames = []
            
            # Record audio
            for i in range(0, int(self.sample_rate / self.chunk_size * duration)):
                data = self.stream.read(self.chunk_size)
                frames.append(data)
            
            logger.info("Recording completed")
            
            # Stop and close stream
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = Path(config.AUDIO_STORAGE_PATH) / f"call_{timestamp}.wav"
            else:
                output_path = Path(output_path)
            
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save to WAV file
            wf = wave.open(str(output_path), 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            logger.info(f"Audio saved to: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Recording failed: {e}")
            raise
    
    def reduce_noise(self, audio_path: str, output_path: str = None) -> str:
        """
        Apply noise reduction to audio file
        
        Args:
            audio_path: Input audio file path
            output_path: Output path for cleaned audio
        
        Returns:
            Path to noise-reduced audio file
        """
        try:
            logger.info(f"Applying noise reduction to: {audio_path}")
            
            # Load audio
            audio_data, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Apply noise reduction
            # Aima: tuned prop_decrease to 0.8 after testing - higher values made speech unclear
            reduced_noise = nr.reduce_noise(
                y=audio_data,
                sr=sr,
                stationary=True,
                prop_decrease=0.8
            )
            
            # Generate output path
            if output_path is None:
                input_path = Path(audio_path)
                output_path = input_path.parent / f"{input_path.stem}_cleaned.wav"
            
            # Save cleaned audio
            sf.write(str(output_path), reduced_noise, sr)
            
            logger.info(f"Noise-reduced audio saved to: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Noise reduction failed: {e}")
            # Return original if noise reduction fails
            return audio_path
    
    def normalize_audio(self, audio_path: str) -> str:
        """
        Normalize audio volume levels
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            Path to normalized audio
        """
        try:
            audio_data, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Normalize to -20 dB
            normalized = librosa.util.normalize(audio_data)
            
            # Overwrite original
            sf.write(audio_path, normalized, sr)
            
            logger.info(f"Audio normalized: {audio_path}")
            return audio_path
            
        except Exception as e:
            logger.error(f"Normalization failed: {e}")
            return audio_path
    
    def process_audio(self, audio_path: str) -> str:
        """
        Complete audio preprocessing pipeline
        
        Args:
            audio_path: Path to raw audio
        
        Returns:
            Path to processed audio
        """
        # Apply noise reduction
        cleaned_path = self.reduce_noise(audio_path)
        
        # Normalize volume
        normalized_path = self.normalize_audio(cleaned_path)
        
        return normalized_path
    
    def load_audio_file(self, file_path: str, output_path: str = None) -> str:
        """
        Load an existing audio file and convert to required format
        
        Args:
            file_path: Path to input audio file
            output_path: Path to save converted file
        
        Returns:
            Path to converted audio file
        """
        try:
            logger.info(f"Loading audio file: {file_path}")
            
            # Load audio
            audio_data, sr = librosa.load(file_path, sr=self.sample_rate)
            
            # Generate output path
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = Path(config.AUDIO_STORAGE_PATH) / f"uploaded_{timestamp}.wav"
            
            # Ensure directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save in standard format
            sf.write(str(output_path), audio_data, sr)
            
            logger.info(f"Audio file loaded and saved to: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Failed to load audio file: {e}")
            raise

