# Development Log - AUTOLEADAI Module 1

Team: Awais Ahmad, Haider Asif, Aima Asghar

---

## October 5, 2025

**Initial Setup**
- Created project structure
- Set up Git repository
- Added basic Python dependencies in requirements.txt
- Researched speech-to-text options: Google Speech API vs Whisper
- Decision: Going with Whisper - better accuracy, runs locally

**Team Meeting Notes:**
- Divided work among team:
  - Awais: Speech-to-text, call logging, database
  - Haider: Spam detection, security features
  - Aima: Audio processing, analytics dashboard

---

## October 8, 2025

**Speech-to-Text Research**
- Installed OpenAI Whisper package
- Tested different model sizes (tiny, base, small)
- Base model seems like good balance - 140MB, decent accuracy
- Issue: Whisper needs ffmpeg but having problems on Windows

---

## October 10, 2025

**Audio Processing Module (Aima)**
- Implemented basic audio loading with librosa
- Added noise reduction using spectral subtraction
- Testing with sample audio files
- Works well but need to fine-tune noise reduction levels

**STT Integration (Awais)**
- Still struggling with ffmpeg on Windows
- Whisper keeps throwing FileNotFoundError
- Tried installing ffmpeg but subprocess.run can't find it
- Need to find workaround

---

## October 12, 2025

**Team Discussion**
- Discussed spam detection approach with Haider
- Options: SVM, Random Forest, or Neural Network
- Decided on Random Forest - simpler, interpretable, good for small dataset
- Need to collect training data for spam/legitimate calls

---

## October 15, 2025

**Web Interface (Team)**
- Started Flask application structure
- Basic HTML template with file upload
- Using Bootstrap for styling
- Need to connect backend processing

**Database Design (Awais)**
- Created SQLite schema for call logs
- Tables: calls, spam_calls, transcripts
- Added foreign key relationships

---

## October 18, 2025

**Spam Detector (Haider)**
- Implemented Random Forest classifier
- Using TF-IDF for feature extraction
- Created training dataset: 15 spam + 15 legitimate examples
- Initial accuracy: 88% (below 90% target)
- Need more training data

---

## October 20, 2025

**Major Breakthrough!**
- Finally fixed Whisper ffmpeg issue!
- Solution: Load audio with librosa first, then pass numpy array to Whisper
- This bypasses the need for ffmpeg subprocess calls
- Transcription now working perfectly on Windows

**Testing:**
- Tested with sample audio files
- Latency: 1.5-2 seconds (meets < 2s requirement)
- Accuracy looks good but need more testing

---

## October 22, 2025

**Noise Reduction (Aima)**
- Improved noise reduction algorithm
- Added audio normalization
- Fixed issue where cleaned audio was too quiet
- Processing pipeline: reduce noise → normalize → save

**Spam Detector Update (Haider)**
- Added more training samples
- Included feature analysis (urgency keywords, free offers, etc.)
- New accuracy: 92% (exceeds 90% target!)

---

## October 25, 2025

**Integration Testing**
- Connected all modules into call_handler.py
- Full pipeline working: audio → preprocessing → STT → spam detection → logging
- Fixed several bugs in error handling
- Average processing time: 5-8 seconds per call

**Call Logger (Awais)**
- Implemented database operations
- Statistics generation working
- Added CSV export functionality

---

## October 28, 2025

**Sample Audio Generation**
- Created script to generate test audio files using gTTS
- Generated 7 sample files (3 legitimate, 4 spam)
- Helps with testing and demonstration

**Web Dashboard Polish**
- Improved UI/UX
- Added real-time statistics display
- Shows transcription, spam status, confidence scores
- Looks professional for demo

---

## October 30, 2025 - Final Day

**Final Testing & Documentation**
- Tested all features end-to-end
- Fixed minor UI bugs
- Cleaned up code comments
- Wrote installation instructions
- Organized documentation files

**Performance Metrics:**
- STT Latency: 1.8s average (target: < 2s) ✓
- Spam Accuracy: 92% (target: ≥ 90%) ✓  
- System works reliably for demo

**Known Issues:**
- First run needs internet to download Whisper model
- Only English language supported
- Training dataset is small (30 samples)

**Ready for demonstration!**

---

## Lessons Learned

1. **ffmpeg compatibility**: Don't assume tools work same on all platforms. Always test on Windows, Linux, Mac.

2. **Early integration**: Should have integrated modules earlier. Found integration bugs late.

3. **Training data matters**: Spam detector improved significantly with more diverse training examples.

4. **Keep it simple**: Initially wanted complex neural network for spam detection. Random Forest works better for our use case.

---

## Future Improvements (Module 2-4)

- Add multi-language support
- Improve spam detector with larger dataset
- Real-time call handling via SIP/VoIP
- Lead qualification logic
- CRM integration

---

**Total Development Time:** ~4 weeks (Oct 5-30)  
**Lines of Code:** ~1,500  
**Commits:** (to be organized)

