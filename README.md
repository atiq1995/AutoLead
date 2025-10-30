# AUTOLEADAI - Module 1: Call Handling and Speech Processing

**Final Year Project 2025-2026**  
Department of Computer Science  
National University of Computer and Emerging Sciences (FAST-NUCES), Islamabad

## Team

- Awais Ahmad (18I-0745)
- Haider Asif (19I-1728)
- Aima Asghar (21I-2772)

**Supervisor:** Mr. Arslan Aslam

---

## Abstract

This module implements an automated call handling system that processes incoming calls, transcribes speech to text, and detects spam using machine learning. The system achieves real-time speech recognition with less than 2 seconds latency and spam detection accuracy of 92%, exceeding the required 90% threshold.

## Problem Statement

Businesses struggle with manual call handling which is time-consuming, expensive, and inconsistent. Spam calls waste resources, and human agents may miss important behavioral cues. This project addresses these issues through AI-powered automation.

## Objectives

1. Automate call reception and processing
2. Implement real-time speech-to-text transcription
3. Detect and filter spam calls using machine learning
4. Log all call data for audit and analysis
5. Provide web-based demonstration interface

## System Architecture

The system consists of five main components:

1. **Audio Processor** - Handles noise reduction and audio normalization
2. **Speech-to-Text Engine** - Uses OpenAI Whisper for transcription
3. **Spam Detector** - ML-based classification using Logistic Regression (TF‑IDF)
4. **Call Logger** - SQLite database for storing call records
5. **Web Interface** - Flask-based demonstration dashboard

## Implementation Details

### Speech Recognition
- OpenAI Whisper (base model)
- Processes audio using librosa to avoid ffmpeg dependency issues
- Sample rate: 16kHz mono

### Spam Detection
- Logistic Regression classifier with TF‑IDF vectorization (word n‑grams)
- Trained from datasets in `Spam Filtering/` (SMS, emails, Enron, etc.)
- Configurable threshold via `.env` (`SPAM_THRESHOLD`)
- Details: see `docs/SPAM_FILTERING.md`

### Audio Processing
- Noise reduction using spectral subtraction
- Volume normalization
- Format conversion for compatibility

## Technologies Used

- Python 3.8+
- OpenAI Whisper - Speech recognition
- scikit-learn - Machine learning
- Flask - Web framework
- librosa - Audio processing
- SQLite - Database

## Installation

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Access dashboard at: http://localhost:5000

## Project Structure

```
├── src/
│   ├── audio_processor.py    # Audio handling
│   ├── speech_to_text.py     # Whisper integration
│   ├── spam_detector.py      # ML classifier
│   ├── call_logger.py        # Database operations
│   └── call_handler.py       # Main pipeline
├── templates/
│   └── index.html            # Web interface
├── sample_audio/             # Test audio files
├── app.py                    # Flask server
├── config.py                 # Configuration
└── requirements.txt          # Dependencies
```

## Results

Performance metrics achieved:

| Metric | Target | Achieved |
|--------|--------|----------|
| Speech-to-Text Latency | < 2s | 1.8s |
| Spam Detection Accuracy | ≥ 90% | 92% |
| System Uptime | ≥ 95% | 99.5% |

## Testing

Sample audio files are provided in `sample_audio/` directory:
- 3 legitimate call examples
- 4 spam call examples

Upload these files through the web interface to test the system.

## Known Issues

1. First run downloads Whisper model (~140MB) - requires internet
2. Processing time varies based on audio length
3. Accuracy depends on audio quality
4. Currently supports English language only

## Challenges Faced

- **ffmpeg compatibility**: Initial Whisper implementation failed on Windows due to ffmpeg dependency. Resolved by using librosa for audio loading.
- **Noise reduction**: Finding the right balance between noise removal and preserving speech quality.
- **Training data**: Limited spam call samples for training the classifier.

## Future Work (Module 2-4)

- Module 2: Lead qualification and dialogue management
- Module 3: Security and prompt injection protection  
- Module 4: Advanced analytics and CRM integration

## Usage

### Web Interface
1. Start server: `python app.py`
2. Open browser: http://localhost:5000
3. Upload audio file or record new call
4. View transcription and spam detection results

### Command Line
```bash
python demo.py path/to/audio.wav
```

## References

1. OpenAI Whisper Documentation
2. scikit-learn User Guide
3. Flask Web Framework Documentation

## License

This project is submitted as part of academic requirements at FAST-NUCES Islamabad.

---

**Contact:**  
For questions or issues, contact the team via university email addresses.

**Last Updated:** October 30, 2025
