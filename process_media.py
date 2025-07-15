#!/usr/bin/env python3
"""
Media Processing Pipeline
Orchestrates video-to-audio conversion, audio cutting, and transcription.
"""

import argparse
import sys
import subprocess
from pathlib import Path

def run_script(script_name, args):
    """Run a script with given arguments."""
    cmd = [sys.executable, script_name] + args
    print(f"🔧 Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}:")
        print(e.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Process media files: video → audio → chunks → transcription")
    
    # Input options
    parser.add_argument("input_file", help="Input video or audio file")
    parser.add_argument("-l", "--language", default="auto", 
                       help="Language for transcription (e.g., 'en', 'ru', 'es') or 'auto' (default: auto)")
    
    # Processing options
    parser.add_argument("--skip-video-conversion", action="store_true",
                       help="Skip video-to-audio conversion (input is already audio)")
    parser.add_argument("--skip-cutting", action="store_true",
                       help="Skip audio cutting (transcribe whole file)")
    parser.add_argument("--skip-transcription", action="store_true",
                       help="Skip transcription (only process audio)")
    
    # Audio cutting options
    parser.add_argument("-d", "--duration", type=int, default=10,
                       help="Duration of audio chunks in minutes (default: 10)")
    
    # Transcription options
    parser.add_argument("-m", "--model", default="base",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("-f", "--format", default="txt",
                       choices=["txt", "json", "srt", "vtt"],
                       help="Transcription output format (default: txt)")
    
    # Output options
    parser.add_argument("-o", "--output-dir", help="Output directory for final results")
    parser.add_argument("--audio-format", default="mp3", 
                       choices=["mp3", "wav", "aac", "flac"],
                       help="Audio format (default: mp3)")
    parser.add_argument("--audio-quality", default="192k",
                       help="Audio quality/bitrate (default: 192k)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    
    # Set up paths
    base_name = input_path.stem
    working_dir = input_path.parent
    
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = working_dir
    
    current_audio_file = None
    
    print(f"🎬 Starting media processing pipeline for: {input_path.name}")
    print(f"📁 Working directory: {working_dir}")
    print(f"📁 Output directory: {output_dir}")
    
    # Step 1: Video to Audio conversion
    if not args.skip_video_conversion:
        print(f"\n=== Step 1: Converting Video to Audio ===")
        audio_file = output_dir / f"{base_name}.{args.audio_format}"
        
        video_args = [
            str(input_path),
            "-o", str(audio_file),
            "-f", args.audio_format,
            "-q", args.audio_quality
        ]
        
        if not run_script("video_to_audio.py", video_args):
            print("❌ Video conversion failed!")
            sys.exit(1)
        
        current_audio_file = audio_file
    else:
        print(f"\n=== Step 1: Skipping Video Conversion ===")
        current_audio_file = input_path
    
    # Step 2: Audio cutting
    if not args.skip_cutting:
        print(f"\n=== Step 2: Cutting Audio into Chunks ===")
        chunks_dir = output_dir / f"{base_name}_chunks"
        
        cutting_args = [
            str(current_audio_file),
            "-d", str(args.duration),
            "-o", str(chunks_dir),
            "-f", args.audio_format
        ]
        
        if not run_script("cut_audio.py", cutting_args):
            print("❌ Audio cutting failed!")
            sys.exit(1)
        
        transcription_input = chunks_dir
    else:
        print(f"\n=== Step 2: Skipping Audio Cutting ===")
        transcription_input = current_audio_file
    
    # Step 3: Transcription
    if not args.skip_transcription:
        print(f"\n=== Step 3: Transcribing Audio ===")
        transcripts_dir = output_dir / f"{base_name}_transcripts"
        
        transcription_args = [
            str(transcription_input),
            "-l", args.language,
            "-m", args.model,
            "-o", str(transcripts_dir),
            "-f", args.format
        ]
        
        if not run_script("transcribe_audio.py", transcription_args):
            print("❌ Transcription failed!")
            sys.exit(1)
    else:
        print(f"\n=== Step 3: Skipping Transcription ===")
    
    print(f"\n🎉 Pipeline completed successfully!")
    print(f"📁 Results saved in: {output_dir}")
    
    # Summary
    print(f"\n📊 Processing Summary:")
    print(f"   Input file: {input_path.name}")
    print(f"   Language: {args.language}")
    print(f"   Model: {args.model}")
    if not args.skip_cutting:
        print(f"   Chunk duration: {args.duration} minutes")
    print(f"   Output format: {args.format}")
    print(f"   Output directory: {output_dir}")

if __name__ == "__main__":
    main()
