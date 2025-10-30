"""
AUTOLEADAI - Setup Script
Quick setup and installation helper
"""
import subprocess
import sys
import os
from pathlib import Path


def print_header():
    print("=" * 60)
    print("  AUTOLEADAI - Module 1 Setup")
    print("  Call Handling & Speech Processing")
    print("=" * 60)
    print()


def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    directories = [
        'data',
        'data/recordings',
        'data/transcripts',
        'data/spam',
        'models',
        'logs',
        'uploads',
        'templates'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")


def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling dependencies...")
    print("This may take several minutes on first run...")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'
        ])
        
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        
        print("✓ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\nSetting up environment configuration...")
    
    env_path = Path('.env')
    if env_path.exists():
        print("  ℹ .env file already exists")
        return
    
    try:
        # Copy from .env.example
        example_path = Path('.env.example')
        if example_path.exists():
            import shutil
            shutil.copy('.env.example', '.env')
            print("  ✓ Created .env from template")
        else:
            # Create basic .env
            with open('.env', 'w') as f:
                f.write("# AUTOLEADAI Configuration\n")
                f.write("DB_PATH=data/autoleadai.db\n")
                f.write("LOG_LEVEL=INFO\n")
                f.write("SAMPLE_RATE=16000\n")
            print("  ✓ Created .env file")
    except Exception as e:
        print(f"  ⚠ Warning: Could not create .env file: {e}")


def download_whisper_model():
    """Pre-download Whisper model"""
    print("\nDownloading Whisper AI model...")
    print("This is a one-time download (~140MB)...")
    
    try:
        import whisper
        whisper.load_model("base")
        print("✓ Whisper model downloaded successfully")
        return True
    except Exception as e:
        print(f"⚠ Warning: Could not download Whisper model: {e}")
        print("  Model will be downloaded on first use")
        return False


def run_tests():
    """Run basic tests"""
    print("\nRunning basic system tests...")
    
    try:
        # Test imports
        import torch
        import whisper
        import sklearn
        import flask
        
        print("✓ All core modules can be imported")
        
        # Test CUDA availability
        if torch.cuda.is_available():
            print("✓ CUDA available - GPU acceleration enabled")
        else:
            print("ℹ CUDA not available - using CPU (slower but works)")
        
        return True
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False


def print_next_steps():
    """Print next steps for user"""
    print("\n" + "=" * 60)
    print("  ✅ SETUP COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("\n1. Activate virtual environment (if not already active):")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Linux/Mac
        print("   source venv/bin/activate")
    
    print("\n2. Start the web dashboard:")
    print("   python app.py")
    print("   Then open: http://localhost:5000")
    
    print("\n3. Or run CLI demo:")
    print("   python demo.py")
    
    print("\n4. Read the documentation:")
    print("   See README.md for detailed usage instructions")
    
    print("\nFor troubleshooting, check README.md or contact the team.")
    print()


def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Download Whisper model
    download_whisper_model()
    
    # Run tests
    run_tests()
    
    # Print next steps
    print_next_steps()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        sys.exit(1)

