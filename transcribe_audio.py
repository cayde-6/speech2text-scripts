#!/usr/bin/env python3
"""
Audio Transcriber
Transcribes audio files using OpenAI Whisper.
"""

import argparse
import os
import sys
import glob
from pathlib import Path
import whisper

def transcribe_audio_files(input_path, language="auto", model="base", output_dir=None, output_format="txt"):
    """
    Transcribe audio files using Whisper.
    
    Args:
        input_path: Path to audio file or directory with audio files
        language: Language code (e.g., 'en', 'ru', 'es') or 'auto' for auto-detection
        model: Whisper model size (tiny, base, small, medium, large)
        output_dir: Output directory for transcripts
        output_format: Output format (txt, json, srt, vtt)
    """
    input_path = Path(input_path)
    
    # Determine audio files to process
    if input_path.is_file():
        # Single file
        audio_files = [input_path]
        if output_dir is None:
            output_dir = input_path.parent / "transcripts"
    elif input_path.is_dir():
        # Directory - find all audio files
        audio_extensions = ['*.mp3', '*.wav', '*.m4a', '*.flac', '*.aac']
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(input_path.glob(ext))
        
        if output_dir is None:
            output_dir = input_path / "transcripts"
    else:
        print(f"❌ Error: Input path '{input_path}' does not exist.")
        return False
    
    if not audio_files:
        print(f"❌ No audio files found in '{input_path}'")
        return False
    
    # Sort files for consistent processing order
    audio_files.sort()
    
    # Create output directory
    output_path = Path(output_dir)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created output directory: {output_dir}")
    except Exception as e:
        print(f"❌ Error creating output directory: {e}")
        return False
    
    # Load Whisper model
    print(f"🤖 Loading Whisper model '{model}'...")
    try:
        whisper_model = whisper.load_model(model)
    except Exception as e:
        print(f"❌ Error loading Whisper model: {e}")
        print("💡 Make sure you have whisper installed: pip install openai-whisper")
        return False
    
    print(f"🎵 Found {len(audio_files)} audio files to transcribe:")
    for file in audio_files:
        print(f"  - {file.name}")
    
    # Transcribe each file
    successful_transcriptions = 0
    for audio_file in audio_files:
        print(f"\n📝 Transcribing: {audio_file.name}")
        
        try:
            # Transcribe with specified or auto-detected language
            transcribe_options = {}
            if language != "auto":
                transcribe_options['language'] = language
            
            result = whisper_model.transcribe(str(audio_file), **transcribe_options)
            
            # Generate output filename
            base_name = audio_file.stem
            if output_format == "txt":
                output_file = output_path / f"{base_name}.txt"
                content = result["text"]
            elif output_format == "json":
                import json
                output_file = output_path / f"{base_name}.json"
                content = json.dumps(result, indent=2, ensure_ascii=False)
            elif output_format == "srt":
                output_file = output_path / f"{base_name}.srt"
                content = generate_srt(result["segments"])
            elif output_format == "vtt":
                output_file = output_path / f"{base_name}.vtt"
                content = generate_vtt(result["segments"])
            else:
                print(f"❌ Unsupported output format: {output_format}")
                continue
            
            # Save transcription
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Show preview and detected language
            detected_language = result.get("language", "unknown")
            preview = result["text"][:100] + "..." if len(result["text"]) > 100 else result["text"]
            
            print(f"✅ Saved: {output_file.name}")
            print(f"🌐 Detected language: {detected_language}")
            print(f"📄 Preview: {preview}")
            
            successful_transcriptions += 1
            
        except Exception as e:
            print(f"❌ Error transcribing {audio_file.name}: {e}")
    
    if successful_transcriptions == len(audio_files):
        print(f"\n🎉 Successfully transcribed all {successful_transcriptions} files!")
        return True
    else:
        print(f"\n⚠️  Transcribed {successful_transcriptions} out of {len(audio_files)} files")
        return False

def generate_srt(segments):
    """Generate SRT format subtitles from Whisper segments."""
    srt_content = ""
    for i, segment in enumerate(segments, 1):
        start_time = format_time_srt(segment["start"])
        end_time = format_time_srt(segment["end"])
        text = segment["text"].strip()
        
        srt_content += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
    
    return srt_content

def generate_vtt(segments):
    """Generate VTT format subtitles from Whisper segments."""
    vtt_content = "WEBVTT\n\n"
    for segment in segments:
        start_time = format_time_vtt(segment["start"])
        end_time = format_time_vtt(segment["end"])
        text = segment["text"].strip()
        
        vtt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    
    return vtt_content

def format_time_srt(seconds):
    """Format time for SRT format (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')

def format_time_vtt(seconds):
    """Format time for VTT format (HH:MM:SS.mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files using Whisper")
    parser.add_argument("input_path", help="Input audio file or directory path")
    parser.add_argument("-l", "--language", default="auto", 
                       help="Language code (e.g., 'en', 'ru', 'es') or 'auto' for auto-detection (default: auto)")
    parser.add_argument("-m", "--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    parser.add_argument("-o", "--output-dir", help="Output directory for transcripts")
    parser.add_argument("-f", "--format", default="txt", 
                       choices=["txt", "json", "srt", "vtt"],
                       help="Output format (default: txt)")
    
    args = parser.parse_args()
    
    success = transcribe_audio_files(
        args.input_path,
        args.language,
        args.model,
        args.output_dir,
        args.format
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
