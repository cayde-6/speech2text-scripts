#!/usr/bin/env python3
"""
Audio Cutter
Cuts audio files into specified duration chunks.
"""

import argparse
import os
import sys
import math
from pathlib import Path
from pydub import AudioSegment

def cut_audio_file(input_file, chunk_duration=10, output_dir=None, output_format="mp3"):
    """
    Cut audio file into chunks of specified duration.
    
    Args:
        input_file: Path to input audio file
        chunk_duration: Duration of each chunk in minutes (default: 10)
        output_dir: Output directory for chunks (default: input_file_chunks)
        output_format: Output format (mp3, wav, etc.)
    """
    input_path = Path(input_file)
    
    # Check if input file exists
    if not input_path.exists():
        print(f"❌ Error: Input file '{input_file}' not found.")
        return False
    
    # Set default output directory
    if output_dir is None:
        output_dir = f"{input_path.stem}_chunks"
    
    output_path = Path(output_dir)
    
    # Create output directory
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created output directory: {output_dir}")
    except Exception as e:
        print(f"❌ Error creating output directory: {e}")
        return False
    
    # Load audio file
    print(f"🎵 Loading audio file: {input_file}")
    try:
        # Try to load based on file extension
        file_ext = input_path.suffix.lower()
        if file_ext == '.mp3':
            audio = AudioSegment.from_mp3(input_file)
        elif file_ext == '.wav':
            audio = AudioSegment.from_wav(input_file)
        elif file_ext == '.m4a':
            audio = AudioSegment.from_file(input_file, format="m4a")
        else:
            # Try to auto-detect format
            audio = AudioSegment.from_file(input_file)
            
    except Exception as e:
        print(f"❌ Error loading audio file: {e}")
        print("💡 Make sure you have the required audio libraries installed:")
        print("   pip install pydub")
        print("   For MP3 support: pip install pydub[mp3]")
        return False
    
    # Calculate chunk parameters
    chunk_duration_ms = chunk_duration * 60 * 1000  # Convert to milliseconds
    total_duration_ms = len(audio)
    total_duration_min = total_duration_ms / 60000
    num_chunks = math.ceil(total_duration_ms / chunk_duration_ms)
    
    print(f"⏱️  Total duration: {total_duration_min:.2f} minutes")
    print(f"✂️  Splitting into {num_chunks} chunks of {chunk_duration} minutes each...")
    
    # Cut and save chunks
    successful_chunks = 0
    for i in range(num_chunks):
        start = i * chunk_duration_ms
        end = min((i + 1) * chunk_duration_ms, total_duration_ms)
        chunk = audio[start:end]
        
        # Generate output filename
        chunk_filename = f"part_{i+1:03d}.{output_format}"
        chunk_path = output_path / chunk_filename
        
        try:
            # Export chunk
            chunk.export(str(chunk_path), format=output_format)
            chunk_duration_actual = (end - start) / 60000
            print(f"✅ Saved: {chunk_filename} ({chunk_duration_actual:.2f} min)")
            successful_chunks += 1
            
        except Exception as e:
            print(f"❌ Error saving chunk {i+1}: {e}")
    
    if successful_chunks == num_chunks:
        print(f"🎉 Successfully created {successful_chunks} audio chunks in '{output_dir}'")
        return True
    else:
        print(f"⚠️  Created {successful_chunks} out of {num_chunks} chunks")
        return False

def main():
    parser = argparse.ArgumentParser(description="Cut audio files into chunks")
    parser.add_argument("input_file", help="Input audio file path")
    parser.add_argument("-d", "--duration", type=int, default=10, 
                       help="Duration of each chunk in minutes (default: 10)")
    parser.add_argument("-o", "--output-dir", help="Output directory for chunks")
    parser.add_argument("-f", "--format", default="mp3", choices=["mp3", "wav", "aac", "flac"], 
                       help="Output format (default: mp3)")
    
    args = parser.parse_args()
    
    success = cut_audio_file(
        args.input_file, 
        args.duration, 
        args.output_dir, 
        args.format
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
