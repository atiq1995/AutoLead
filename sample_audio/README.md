# AUTOLEADAI Sample Audio Files

This folder contains 7 sample audio files for testing Module 1.

## Files Overview

### Legitimate Calls (3 files)

**legitimate_call_1.mp3**
- Real estate inquiry - serious buyer
- Script: "Hello, I'm calling about the real estate listing I saw online. I'm interested in scheduling a viewin..."

**legitimate_call_2.mp3**
- Business inquiry - software development
- Script: "Good morning. I saw your advertisement for software development services. Our company needs a custom..."

**legitimate_call_3.mp3**
- Wholesale inquiry - retail business
- Script: "Hi, I'm interested in your product catalog. I run a retail business and I'm looking for wholesale su..."

### Spam Calls (4 files)

**spam_call_1.mp3**
- Prize scam - urgency and free offers
- Script: "Congratulations! You have been selected as our lucky winner today! You've won a free vacation packag..."

**spam_call_2.mp3**
- Debt collection scam - threats and urgency
- Script: "This is an urgent message regarding your outstanding debt. You owe thousands of dollars and must cal..."

**spam_call_3.mp3**
- Tech support scam - fear and urgency
- Script: "Warning! We have detected a serious virus on your computer. Your personal information and credit car..."

**spam_call_4.mp3**
- Get-rich-quick scam - unrealistic promises
- Script: "Exclusive limited time offer! Get rich quick with our amazing money-making system! Earn thousands of..."

## How to Use

1. Start the web demo: `python app.py`
2. Open: http://localhost:5000
3. Click "Choose Audio File"
4. Select any file from this folder
5. Click "Process Call"
6. View results!

## Expected Results

- **Legitimate calls**: Should be classified as NOT SPAM
- **Spam calls**: Should be detected with high confidence (>70%)

## Notes

- Files are in MP3 format (supported by the system)
- Generated using Google Text-to-Speech
- Voices are synthetic but clear enough for testing
