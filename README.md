# Speech-to-Text Processing Scripts

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A set of modular Python scripts for processing video and audio files: conversion, cutting, and transcription using OpenAI Whisper.

## 🤖 About OpenAI Whisper

[OpenAI Whisper](https://github.com/openai/whisper) is a robust speech recognition model that:
- Supports 99+ languages with high accuracy
- Works offline (no internet required after installation)
- Provides multiple model sizes for different speed/accuracy tradeoffs
- Can generate transcripts, subtitles (SRT/VTT), and timestamps
- Handles various audio formats and quality levels

These scripts make Whisper easy to use for batch processing and large media files.

## 🚀 Quick Start

```bash
# Process a video file with English transcription
python3 process_media.py video.mp4 -l en

# Process audio-only file with Russian transcription
python3 process_media.py audio.mp3 --skip-video-conversion -l ru
```

## 📋 Scripts Overview

### 1. `video_to_audio.py`
Converts video files to audio format using FFmpeg.

### 2. `cut_audio.py`
Cuts audio files into chunks of specified duration.

### 3. `transcribe_audio.py`
Transcribes audio files using OpenAI Whisper with configurable language settings.

### 4. `process_media.py`
Main pipeline script that orchestrates the entire workflow.

## 🔧 Installation

### Prerequisites
- **Python 3.8+** (recommended: Python 3.9 or higher)
- **FFmpeg** (for video processing)

### Step 1: Clone the Repository
```bash
git clone https://github.com/cayde-6/speech2text-scripts.git
cd speech2text-scripts
```

### Step 2: Install System Dependencies

> **Note**: These scripts have been tested on macOS. For Linux/Windows, you can try installing FFmpeg via your system's package manager (apt, yum, chocolatey, etc.).

#### macOS
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install FFmpeg
brew install ffmpeg

# Verify installation
ffmpeg -version
```

#### Other Platforms
- **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)
- **Windows**: `choco install ffmpeg` (Chocolatey) or download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Step 3: Install Python Dependencies

```bash
# Option 1: Install from requirements.txt (recommended)
pip install -r requirements.txt

# Option 2: Install manually
pip install openai-whisper pydub[mp3] torch torchvision torchaudio
```

## Usage Examples

### Full Pipeline (Video → Audio → Chunks → Transcription)

```bash
# Process a video file with Russian transcription
python3 process_media.py video.mp4 -l ru

# Process with custom settings
python3 process_media.py video.mp4 -l en -m small -d 5 -f srt -o results/
```

### Individual Scripts

#### Video to Audio Conversion
```bash
# Convert video to MP3
python3 video_to_audio.py input.mp4 -o output.mp3

# Convert with different quality and format
python3 video_to_audio.py input.mp4 -f wav -q 320k

# Force overwrite existing files without prompting
python3 video_to_audio.py input.mp4 -o output.mp3 --force
```

#### Audio Cutting
```bash
# Cut audio into 10-minute chunks (default)
python3 cut_audio.py audio.mp3

# Cut into 5-minute chunks with custom output directory
python3 cut_audio.py audio.mp3 -d 5 -o chunks/

# Cut and convert format
python3 cut_audio.py input.wav -f mp3 -o mp3_chunks/
```

#### Audio Transcription
```bash
# Transcribe all audio files in current directory with Russian language
python3 transcribe_audio.py . -l ru

# Transcribe single file with auto language detection
python3 transcribe_audio.py audio.mp3 -l auto

# Transcribe with larger model and SRT output
python3 transcribe_audio.py chunks/ -l en -m large -f srt
```

## Pipeline Options

### Main Pipeline (`process_media.py`)

**Basic usage:**
```bash
python3 process_media.py <input_file> [options]
```

**Key options:**
- `-l, --language`: Language code (en, ru, es, etc.) or 'auto' (default: auto)
- `-m, --model`: Whisper model size (tiny, base, small, medium, large)
- `-d, --duration`: Chunk duration in minutes (default: 10)
- `-f, --format`: Output format (txt, json, srt, vtt)
- `-o, --output-dir`: Output directory

**Skip options:**
- `--skip-video-conversion`: Skip video conversion (input is already audio)
- `--skip-cutting`: Skip audio cutting (transcribe whole file)
- `--skip-transcription`: Skip transcription (only process audio)

## Common Use Cases

### 1. Process video with Russian transcription
```bash
python3 process_media.py video.mp4 -l ru
```

### 2. Process only audio file (skip video conversion)
```bash
python3 process_media.py audio.mp3 --skip-video-conversion -l en
```

### 3. Cut audio without transcription
```bash
python3 process_media.py audio.mp3 --skip-video-conversion --skip-transcription -d 15
```

### 4. Transcribe without cutting (whole file)
```bash
python3 process_media.py video.mp4 --skip-cutting -l auto -m medium
```

### 5. Generate subtitles
```bash
python3 process_media.py video.mp4 -l en -f srt --skip-cutting
```

## Language Codes

Common language codes for transcription:
- `auto`: Auto-detect language
- `en`: English
- `ru`: Russian
- `es`: Spanish
- `fr`: French
- `de`: German
- `zh`: Chinese
- `ja`: Japanese
- `ko`: Korean

## Whisper Model Sizes

- `tiny`: Fastest, least accurate (~1GB VRAM)
- `base`: Good balance (default) (~1GB VRAM)
- `small`: Better accuracy (~2GB VRAM)
- `medium`: High accuracy (~5GB VRAM)
- `large`: Best accuracy (~10GB VRAM)

## Output Structure

```
output_directory/
├── video_name.mp3              # Converted audio (if from video)
├── video_name_chunks/          # Audio chunks directory
│   ├── part_001.mp3
│   ├── part_002.mp3
│   └── ...
└── video_name_transcripts/     # Transcription results
    ├── part_001.txt
    ├── part_002.txt
    └── ...
```

## 🆕 Recent Improvements

### v1.1.0 - Pipeline Automation Fix
- **Fixed**: Interactive prompt issue in `process_media.py` pipeline
- **Added**: `--force` flag to `video_to_audio.py` for automatic file overwriting
- **Improved**: Pipeline now runs completely non-interactively
- **Enhanced**: Better error handling and user experience

### What was fixed:
Previously, the pipeline would hang when output files already existed due to interactive "Overwrite? (y/N)" prompts. Now the pipeline automatically overwrites existing files during processing, making it suitable for automated workflows and re-runs.

## 🐛 Troubleshooting

### Pipeline hangs or gets interrupted
- **Solution**: Update to latest version - this issue has been fixed
- **Workaround**: Use individual scripts with `--force` flag when needed

### Missing dependencies
```bash
# Install missing PyTorch (required for Whisper)
pip install torch torchvision torchaudio

# Install missing audio processing libraries
pip install pydub[mp3]
```

### FFmpeg not found
```bash
# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```
