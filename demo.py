"""
AUTOLEADAI - Quick Demo Script
Simple command-line demo for Module 1
Author: Team AUTOLEADAI
"""
import sys
import logging
from pathlib import Path
from colorama import Fore, Style, init
from src.call_handler import CallHandler

# Initialize colorama
init()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print demo banner"""
    print(Fore.CYAN + "=" * 60)
    print("  🤖 AUTOLEADAI - Module 1 Demo")
    print("  Call Handling & Speech Processing with Spam Filtering")
    print("  FAST-NUCES Islamabad | FYP 2025-2026")
    print("=" * 60 + Style.RESET_ALL)
    print()


def print_result(result):
    """Print formatted result"""
    if not result.get('success'):
        print(Fore.RED + f"❌ Error: {result.get('error')}" + Style.RESET_ALL)
        return
    
    print()
    print(Fore.CYAN + "=" * 60)
    print("📊 CALL PROCESSING RESULT")
    print("=" * 60 + Style.RESET_ALL)
    
    # Spam status
    if result['is_spam']:
        print(Fore.RED + "🚫 STATUS: SPAM CALL DETECTED" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "✅ STATUS: LEGITIMATE CALL" + Style.RESET_ALL)
    
    print(f"\n📋 Call ID: {result['call_id']}")
    print(f"⏱️  Processing Time: {result['processing_time']:.2f} seconds")
    print(f"📊 Spam Confidence: {result['spam_confidence']:.2%}")
    
    # Transcript
    print(f"\n📝 Transcript:")
    print(Fore.YELLOW + "-" * 60)
    print(result['transcript'])
    print("-" * 60 + Style.RESET_ALL)
    
    # Spam features
    if result['is_spam'] and result.get('spam_features'):
        print(f"\n⚠️  Detected Spam Indicators:")
        for category, info in result['spam_features'].items():
            if info['detected'] and info['keywords']:
                print(f"  • {category}: {', '.join(info['keywords'])}")
    
    print()


def main():
    """Main demo function"""
    print_banner()
    
    # Initialize call handler
    print(Fore.YELLOW + "Initializing AUTOLEADAI Module 1..." + Style.RESET_ALL)
    call_handler = CallHandler()
    print(Fore.GREEN + "✓ System initialized\n" + Style.RESET_ALL)
    
    # Get audio file path
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
    else:
        print(Fore.CYAN + "Enter path to audio file (or press Enter for demo recording): " + Style.RESET_ALL, end='')
        audio_path = input().strip()
    
    # Process call
    if audio_path and Path(audio_path).exists():
        print(f"\n{Fore.YELLOW}Processing audio file: {audio_path}{Style.RESET_ALL}")
        result = call_handler.process_call(audio_path, source_type='file')
    else:
        print(f"\n{Fore.YELLOW}Recording audio for 10 seconds...{Style.RESET_ALL}")
        print(Fore.RED + "Speak now!" + Style.RESET_ALL)
        result = call_handler.process_call("10", source_type='record')
    
    # Display result
    print_result(result)
    
    # Show statistics
    stats = call_handler.get_call_statistics()
    print(Fore.CYAN + "=" * 60)
    print("📈 SYSTEM STATISTICS")
    print("=" * 60 + Style.RESET_ALL)
    print(f"Total Calls: {stats['total_calls']}")
    print(f"Spam Calls: {stats['spam_calls']}")
    print(f"Legitimate Calls: {stats['legitimate_calls']}")
    print(f"Spam Rate: {stats['spam_rate']:.1f}%")
    print()
    
    print(Fore.GREEN + "Demo completed successfully! ✓" + Style.RESET_ALL)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Demo interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        logger.exception("Demo failed")

