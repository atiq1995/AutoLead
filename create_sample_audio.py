"""
AUTOLEADAI - Sample Audio Generator
Creates sample audio files for testing and demonstration
Author: Team AUTOLEADAI

Note: This script requires gTTS (Google Text-to-Speech)
Install with: pip install gTTS
"""
import os
from pathlib import Path

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("Warning: gTTS not installed. Install with: pip install gTTS")


# Sample scripts
SAMPLE_CALLS = {
    "legitimate_call_1.mp3": {
        "text": "Hello, I'm calling about the real estate listing I saw online. I'm interested in scheduling a viewing of the two-bedroom apartment in DHA Phase 5. Could you tell me more about the price and location? My budget is around 25 million rupees. I'm a serious buyer looking to purchase within the next month. Please call me back at your earliest convenience.",
        "type": "legitimate",
        "description": "Real estate inquiry - serious buyer"
    },
    
    "legitimate_call_2.mp3": {
        "text": "Good morning. I saw your advertisement for software development services. Our company needs a custom CRM system and we're looking for a reliable development partner. Can you provide information about your pricing, timeline, and previous projects? We'd like to schedule a meeting next week to discuss requirements in detail.",
        "type": "legitimate",
        "description": "Business inquiry - software development"
    },
    
    "legitimate_call_3.mp3": {
        "text": "Hi, I'm interested in your product catalog. I run a retail business and I'm looking for wholesale suppliers. Can you send me your price list and minimum order quantities? I've been in business for five years and I'm looking to establish a long-term partnership. Thank you.",
        "type": "legitimate",
        "description": "Wholesale inquiry - retail business"
    },
    
    "spam_call_1.mp3": {
        "text": "Congratulations! You have been selected as our lucky winner today! You've won a free vacation package worth five thousand dollars! This is a limited time offer and you must act now to claim your amazing prize! Call us immediately at this number to verify your winning entry. Don't miss this once in a lifetime opportunity! Call now before it's too late!",
        "type": "spam",
        "description": "Prize scam - urgency and free offers"
    },
    
    "spam_call_2.mp3": {
        "text": "This is an urgent message regarding your outstanding debt. You owe thousands of dollars and must call us immediately to avoid legal action. Your account will be sent to collections if you don't respond today. This is your final warning. Failure to contact us will result in wage garnishment and asset seizure. Call now!",
        "type": "spam",
        "description": "Debt collection scam - threats and urgency"
    },
    
    "spam_call_3.mp3": {
        "text": "Warning! We have detected a serious virus on your computer. Your personal information and credit card details are at risk. Your system is compromised and hackers may be stealing your data right now. Call our technical support team immediately for free assistance. Don't delay, your computer could crash at any moment. Call now to protect your information!",
        "type": "spam",
        "description": "Tech support scam - fear and urgency"
    },
    
    "spam_call_4.mp3": {
        "text": "Exclusive limited time offer! Get rich quick with our amazing money-making system! Earn thousands of dollars from home with zero effort! Act now and we'll give you a special discount! This offer expires today! Free money waiting for you! Call immediately to claim your free cash bonus!",
        "type": "spam",
        "description": "Get-rich-quick scam - unrealistic promises"
    }
}


def create_sample_audio_files():
    """Create sample audio files using Google Text-to-Speech"""
    
    if not GTTS_AVAILABLE:
        print("\n❌ Error: gTTS library not installed")
        print("\nTo install:")
        print("  pip install gTTS")
        print("\nOr manually create audio files with the scripts provided in the code.")
        return False
    
    # Create samples directory
    samples_dir = Path("sample_audio")
    samples_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("  AUTOLEADAI - Sample Audio Generator")
    print("=" * 60)
    print(f"\nCreating {len(SAMPLE_CALLS)} sample audio files...")
    print(f"Output directory: {samples_dir.absolute()}\n")
    
    legitimate_count = 0
    spam_count = 0
    
    for filename, data in SAMPLE_CALLS.items():
        try:
            print(f"Creating: {filename}")
            print(f"  Type: {data['type']}")
            print(f"  Description: {data['description']}")
            
            # Generate speech
            tts = gTTS(text=data['text'], lang='en', slow=False)
            
            # Save file
            output_path = samples_dir / filename
            tts.save(str(output_path))
            
            print(f"  [OK] Saved to: {output_path}")
            print()
            
            if data['type'] == 'legitimate':
                legitimate_count += 1
            else:
                spam_count += 1
                
        except Exception as e:
            print(f"  [ERROR] Error creating {filename}: {e}")
            print()
    
    # Create README in samples directory
    readme_content = f"""# AUTOLEADAI Sample Audio Files

This folder contains {len(SAMPLE_CALLS)} sample audio files for testing Module 1.

## Files Overview

### Legitimate Calls ({legitimate_count} files)
"""
    
    for filename, data in SAMPLE_CALLS.items():
        if data['type'] == 'legitimate':
            readme_content += f"\n**{filename}**\n"
            readme_content += f"- {data['description']}\n"
            readme_content += f"- Script: \"{data['text'][:100]}...\"\n"
    
    readme_content += f"\n### Spam Calls ({spam_count} files)\n"
    
    for filename, data in SAMPLE_CALLS.items():
        if data['type'] == 'spam':
            readme_content += f"\n**{filename}**\n"
            readme_content += f"- {data['description']}\n"
            readme_content += f"- Script: \"{data['text'][:100]}...\"\n"
    
    readme_content += """
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
"""
    
    readme_path = samples_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("=" * 60)
    print("[SUCCESS] Sample Audio Generation Complete!")
    print("=" * 60)
    print(f"\nCreated {len(SAMPLE_CALLS)} audio files:")
    print(f"  - {legitimate_count} legitimate calls")
    print(f"  - {spam_count} spam calls")
    print(f"\nFiles saved to: {samples_dir.absolute()}")
    print(f"\nUse these files to test the system!")
    print("\nTo test:")
    print("  1. python app.py")
    print("  2. Open http://localhost:5000")
    print("  3. Upload files from sample_audio/ folder")
    print()
    
    return True


def print_scripts():
    """Print all scripts for manual recording"""
    print("\n" + "=" * 60)
    print("  Sample Call Scripts")
    print("  (Use these if you want to record audio manually)")
    print("=" * 60)
    
    for filename, data in SAMPLE_CALLS.items():
        print(f"\n{'='*60}")
        print(f"File: {filename}")
        print(f"Type: {data['type'].upper()}")
        print(f"Description: {data['description']}")
        print(f"{'='*60}")
        print(f"\n{data['text']}\n")


if __name__ == '__main__':
    import sys
    
    if '--scripts' in sys.argv or '--text' in sys.argv:
        # Just print scripts for manual recording
        print_scripts()
    else:
        # Generate audio files
        success = create_sample_audio_files()
        
        if not success:
            print("\nAlternatively, run with --scripts to see text scripts:")
            print("  python create_sample_audio.py --scripts")

