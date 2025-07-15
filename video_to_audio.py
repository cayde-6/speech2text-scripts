#!/usr/bin/env python3
"""
Video to Audio Converter
Converts video files to audio format using FFmpeg.
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

def convert_video_to_audio(input_file, output_file=None, audio_format="mp3", quality="192k"):
    """
    Convert video file to audio format.
    
    Args:
        input_file: Path to input video file
        output_file: Path to output audio file (optional)
        audio_format: Audio format (mp3, wav, etc.)
        quality: Audio quality/bitrate
    """
    input_path = Path(input_file)
    
    # Check if input file exists
    if not input_path.exists():
        print(f"❌ Error: Input file '{input_file}' not found.")
        return False
    
    # Generate output filename if not provided
    if output_file is None:
        output_file = input_path.stem + f".{audio_format}"
    
    output_path = Path(output_file)
    
    # Check if output file already exists
    if output_path.exists():
        response = input(f"⚠️  Output file '{output_file}' already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Operation cancelled.")
            return False
    
    print(f"🎬 Converting '{input_file}' to '{output_file}'...")
    
    # FFmpeg command
    cmd = [
        "ffmpeg",
        "-i", str(input_path),
        "-vn",  # No video
        "-acodec", "libmp3lame" if audio_format == "mp3" else "copy",
        "-ab", quality,
        "-y",  # Overwrite output file
        str(output_path)
    ]
    
    try:
        # Run FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Successfully converted to: {output_file}")
            return True
        else:
            print(f"❌ FFmpeg error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Error: FFmpeg not found. Please install FFmpeg first.")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt-get install ffmpeg")
        return False
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Convert video files to audio format")
    parser.add_argument("input_file", help="Input video file path")
    parser.add_argument("-o", "--output", help="Output audio file path (optional)")
    parser.add_argument("-f", "--format", default="mp3", choices=["mp3", "wav", "aac", "flac"], 
                       help="Output audio format (default: mp3)")
    parser.add_argument("-q", "--quality", default="192k", 
                       help="Audio quality/bitrate (default: 192k)")
    
    args = parser.parse_args()
    
    success = convert_video_to_audio(
        args.input_file, 
        args.output, 
        args.format, 
        args.quality
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
