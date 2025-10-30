"""
AUTOLEADAI - Module 1 Configuration
Central configuration file for all module settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Database Configuration
DB_PATH = os.getenv('DB_PATH', 'data/autoleadai.db')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_PATH = os.getenv('LOG_PATH', 'logs/')

# Audio Settings
SAMPLE_RATE = int(os.getenv('SAMPLE_RATE', 16000))
AUDIO_FORMAT = os.getenv('AUDIO_FORMAT', 'wav')
CHANNELS = 1  # Mono audio

# Spam Detection
SPAM_THRESHOLD = float(os.getenv('SPAM_THRESHOLD', 0.7))
SPAM_MODEL_PATH = 'models/spam_detector.pkl'
SPAM_VECTORIZER_PATH = 'models/vectorizer.pkl'

# Storage Paths
AUDIO_STORAGE_PATH = os.getenv('AUDIO_STORAGE_PATH', 'data/recordings/')
TRANSCRIPTS_PATH = os.getenv('TRANSCRIPTS_PATH', 'data/transcripts/')
SPAM_STORAGE_PATH = os.getenv('SPAM_STORAGE_PATH', 'data/spam/')

# Whisper Model Settings
WHISPER_MODEL = 'base'  # Options: tiny, base, small, medium, large
WHISPER_LANGUAGE = 'en'

# Create necessary directories
for path in [LOG_PATH, AUDIO_STORAGE_PATH, TRANSCRIPTS_PATH, SPAM_STORAGE_PATH, 'models', 'data']:
    Path(path).mkdir(parents=True, exist_ok=True)

