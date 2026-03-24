import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Monkey patch for MoviePy 1.0.3 compatibility with Pillow >= 10.0.0
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = getattr(Image, 'LANCZOS', 1)

from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, vfx

def create_text_image(text, size=(1080, 1920), font_size=80, color=(255, 255, 255), stroke_color=(0, 0, 0), stroke_width=4):
    """
    Creates an image with centered text using Pillow. This avoids ImageMagick requirements on Windows.
    Returns a numpy array representing the image.
    """
    # Create a transparent image
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Try to load a nice font, fallback to default
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size) # Arial Bold
    except IOError:
        font = ImageFont.load_default()

    # Calculate text bounding box for centering
    # Split text into lines if it's too long
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        # Approximate width check based on font size. Better to use getbbox but this is safer with varying PIL versions
        if len(' '.join(current_line)) * (font_size * 0.5) > size[0] * 0.8:
            lines.append(' '.join(current_line[:-1]))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
        
    final_text = "\n".join(lines)
    
    # Text positioning (center of screen)
    bbox = d.textbbox((0, 0), final_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) / 2
    y = (size[1] - text_height) / 2
    
    # Draw text with stroke for visibility
    d.text((x, y), final_text, font=font, fill=color, stroke_width=stroke_width, stroke_fill=stroke_color, align="center")
    
    return np.array(img)

def generate_subtitle_clips(text, audio_duration, video_size=(1080, 1920)):
    """
    Splits text into chunks and creates synchronized ImageClips.
    """
    # Simple chunking: ~5 words per subtitle
    words = text.split()
    chunks = []
    chunk_size = 5
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
        
    num_chunks = len(chunks)
    time_per_chunk = audio_duration / num_chunks if num_chunks > 0 else 0
    
    subtitle_clips = []
    current_time = 0
    
    for chunk in chunks:
        # Create image array with PIL
        img_array = create_text_image(chunk, size=video_size)
        
        # Create MoviePy clip from numpy array
        clip = ImageClip(img_array).set_start(current_time).set_duration(time_per_chunk).set_position('center')
        subtitle_clips.append(clip)
        current_time += time_per_chunk
        
    return subtitle_clips

def assemble_video(audio_path, background_video_path, story_text, output_path="final_video.mp4"):
    """
    Assembles the final video by combining background, audio, and subtitles.
    """
    print(f"Loading audio from {audio_path}...")
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    
    print(f"Loading background video from {background_video_path}...")
    try:
        bg_clip = VideoFileClip(background_video_path)
    except Exception as e:
        print(f"Error loading background video: {e}")
        print("Please ensure you have a valid background video file.")
        return False
        
    # Crop to 9:16 aspect ratio (YouTube Shorts) - assuming 1920x1080 horizontal video input
    w, h = bg_clip.size
    target_w = h * 9 / 16
    x_center = w / 2
    bg_clip = bg_clip.crop(x1=x_center - target_w/2, y1=0, x2=x_center + target_w/2, y2=h)
    bg_clip = bg_clip.resize((1080, 1920))
    video_size = bg_clip.size
    
    # Loop or cut background video to match audio length
    if bg_clip.duration < audio_duration:
        print("Background video is shorter than audio. Looping...")
        # vfx.loop requires looping multiple times, let's just do a simple subclip approach or loop
        num_loops = math.ceil(audio_duration / bg_clip.duration)
        bg_clip = bg_clip.fx(vfx.loop, duration=audio_duration)
    else:
        print("Trimming background video...")
        # Take a random subclip if possible, but for simplicity we'll just take the start
        bg_clip = bg_clip.subclip(0, audio_duration)
        
    # Set the audio
    bg_clip = bg_clip.set_audio(audio_clip)
    
    # Generate subtitle clips
    print("Generating subtitles...")
    subtitle_clips = generate_subtitle_clips(story_text, audio_duration, video_size)
    
    # Composite
    print("Compositing final video...")
    final_video = CompositeVideoClip([bg_clip] + subtitle_clips)
    
    # Render
    print(f"Rendering to {output_path}...")
    final_video.write_videofile(
        output_path, 
        fps=30, 
        codec="libx264", 
        audio_codec="aac", 
        threads=4,
        preset="ultrafast" # Use ultrafast for testing, can change to medium later
    )
    
    print("Video rendering complete!")
    return True

if __name__ == "__main__":
    # A simple test (requires a test_audio.mp3 and a test_bg.mp4)
    print("To test the video assembly, run main.py once everything is set up.")
