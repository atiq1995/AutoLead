# AUTOLEADAI Module 1 - Installation Guide

## 🚀 Quick Start (5 Minutes)

### Windows Installation

1. **Open PowerShell or Command Prompt**
   - Press `Win + R`, type `cmd`, press Enter

2. **Navigate to project folder**
   ```cmd
   cd "D:\Project\Awais Final project"
   ```

3. **Create virtual environment**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Run setup script**
   ```cmd
   python setup.py
   ```

5. **Start the application**
   ```cmd
   python app.py
   ```

6. **Open browser**
   ```
   http://localhost:5000
   ```

---

## 📋 Detailed Installation Steps

### Prerequisites

#### 1. Install Python 3.8+

**Check if Python is installed:**
```cmd
python --version
```

**If not installed:**
- Download from: https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Restart computer after installation

#### 2. Install Git (Optional)

Download from: https://git-scm.com/download/win

---

### Step-by-Step Installation

#### Step 1: Create Virtual Environment

```cmd
cd "D:\Project\Awais Final project"
python -m venv venv
```

#### Step 2: Activate Virtual Environment

**Windows:**
```cmd
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

#### Step 3: Upgrade pip

```cmd
python -m pip install --upgrade pip
```

#### Step 4: Install Dependencies

```cmd
pip install -r requirements.txt
```

**This will take 5-10 minutes** as it downloads:
- PyTorch (~800MB)
- Whisper AI model
- Other dependencies

#### Step 5: Verify Installation

```cmd
python setup.py
```

This will:
- ✅ Check Python version
- ✅ Create necessary folders
- ✅ Download AI models
- ✅ Run tests

---

## 🎮 Running the Application

### Option 1: Web Dashboard (Recommended)

```cmd
python app.py
```

Then open browser: http://localhost:5000

### Option 2: Command Line Demo

```cmd
python demo.py
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: "pip is not recognized"

**Solution:**
```cmd
python -m pip install -r requirements.txt
```

### Issue 2: "No module named 'pyaudio'"

**Windows Solution:**
```cmd
pip install pipwin
pipwin install pyaudio
```

**Linux Solution:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Mac Solution:**
```bash
brew install portaudio
pip install pyaudio
```

### Issue 3: PyTorch Installation Fails

**Windows (CPU-only):**
```cmd
pip install torch torchvision torchaudio
```

**If still fails:**
```cmd
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cpu
```

### Issue 4: "Permission Denied"

**Windows:** Run Command Prompt as Administrator

**Linux/Mac:**
```bash
sudo pip install -r requirements.txt
```

### Issue 5: Whisper Model Download Fails

**Manual download:**
1. Visit: https://github.com/openai/whisper
2. Download `base` model
3. Place in: `~/.cache/whisper/`

### Issue 6: Flask Port Already in Use

Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Use 8080 instead of 5000
```

---

## 🧪 Testing Installation

### Test 1: Check Imports

```python
python -c "import whisper; import torch; import sklearn; print('All imports successful!')"
```

### Test 2: Run Demo

```cmd
python demo.py
```

### Test 3: Check CUDA (GPU)

```python
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

---

## 📦 Manual Dependency Installation

If automated installation fails, install manually:

```cmd
pip install openai-whisper
pip install torch torchvision torchaudio
pip install pyaudio soundfile librosa noisereduce
pip install scikit-learn numpy pandas
pip install flask flask-cors
pip install sqlalchemy python-dotenv colorama
```

---

## 🔧 System Requirements

### Minimum:
- **OS:** Windows 10, Ubuntu 20.04, macOS 10.15
- **Python:** 3.8+
- **RAM:** 4GB
- **Disk:** 2GB free space
- **Internet:** For initial model download

### Recommended:
- **RAM:** 8GB+
- **CPU:** Intel i5 or equivalent
- **GPU:** NVIDIA GPU with CUDA (optional, for faster processing)

---

## 🌐 Network Requirements

### Required Downloads (First Run):
- Whisper base model: ~140MB
- PyTorch: ~800MB (if not installed)
- Other dependencies: ~200MB

**Total:** ~1.2GB download

### Firewall Settings:
- Allow Python through firewall
- Open port 5000 for Flask (if using web dashboard)

---

## 📱 Windows Defender / Antivirus

Some antivirus software may flag Python scripts:

1. Add Python to exclusions:
   - Open Windows Security
   - Virus & threat protection
   - Manage settings
   - Exclusions → Add → Folder
   - Select: `D:\Project\Awais Final project`

---

## 🔄 Updating the Application

```cmd
# Activate venv
venv\Scripts\activate

# Pull latest changes (if using Git)
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Run setup again
python setup.py
```

---

## 🗑️ Uninstallation

```cmd
# Deactivate virtual environment
deactivate

# Delete project folder
cd ..
rmdir /s "Awais Final project"
```

---

## 💡 Tips for Demonstration

1. **Prepare test audio files** before demo
2. **Pre-download models** by running setup
3. **Test microphone** if doing live recording
4. **Close other heavy applications** for better performance
5. **Have backup slides** in case of technical issues

---

## 📞 Getting Help

### Documentation:
- README.md - User guide
- INSTALLATION.md - This file
- Code comments - Implementation details

### Contact Team:
- Awais Ahmad: 18i-0745@fast.nu.edu.pk
- Haider Asif: 19i-1728@fast.nu.edu.pk
- Aima Asghar: 21i-2772@fast.nu.edu.pk

### Debugging:
```cmd
# Enable verbose logging
set LOG_LEVEL=DEBUG
python app.py
```

---

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Whisper model downloaded
- [ ] Setup script ran successfully
- [ ] Test imports work
- [ ] Web dashboard opens
- [ ] Sample audio processed

---

**Last Updated:** October 30, 2025  
**Version:** 1.0.0

