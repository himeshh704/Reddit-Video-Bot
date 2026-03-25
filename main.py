import os
import sys
import time

from reddit_scraper import get_top_story
from audio_generator import generate_audio
from video_editor import assemble_video
from youtube_uploader import get_authenticated_service, upload_video

# You must place a video file named 'background.mp4' in this directory before running
BACKGROUND_VIDEO = "background.mp4"
AUDIO_OUTPUT = "temp_audio.mp3"
FINAL_VIDEO = "final_short.mp4"

def main():
    print("=== Automated Reddit Story Video Generator ===")
    
    # 1. Check for background video
    if not os.path.exists(BACKGROUND_VIDEO):
        print(f"ERROR: {BACKGROUND_VIDEO} not found.")
        print("Please download a background video (e.g., Minecraft parkour, GTA racing)")
        print(f"and save it as '{BACKGROUND_VIDEO}' in this directory.")
        sys.exit(1)
        
    # 2. Scrape Story
    print("\n--- STEP 1: Scraping Reddit Story ---")
    story = get_top_story(subreddit_name="TwoSentenceHorror", time_filter="month", min_length=50, max_length=950) # Very short Shorts
    
    if not story:
        print("Failed to find a suitable story.")
        sys.exit(1)
        
    title = story["title"]
    text = story["text"]
    print(f"Successfully scraped: {title}")
    
    # 3. Generate Audio
    print("\n--- STEP 2: Generating Text-to-Speech ---")
    generate_audio(text, AUDIO_OUTPUT)
    
    if not os.path.exists(AUDIO_OUTPUT):
        print("Failed to generate audio.")
        sys.exit(1)
        
    # 4. Assemble Video
    print("\n--- STEP 3: Assembling Video ---")
    success = assemble_video(AUDIO_OUTPUT, BACKGROUND_VIDEO, text, FINAL_VIDEO)
    
    if not success or not os.path.exists(FINAL_VIDEO):
        print("Failed to assemble video.")
        sys.exit(1)
        
    # 5. Upload to YouTube (Optional/Commented out by default to avoid accidental uploads)
    print("\n--- STEP 4: YouTube Upload ---")
    print("Video generation complete!")
    print(f"Your video is saved as {FINAL_VIDEO}.")
    
    print("Attempting to upload to YouTube...")
    youtube_service = get_authenticated_service()
    if youtube_service:
        # Ensure we don't exceed YouTube title limits
        safe_title = title[:95] + "..." if len(title) > 95 else title
        upload_video(youtube_service, FINAL_VIDEO, safe_title, text)
    else:
        print("Failed to authenticate with YouTube.")

if __name__ == "__main__":
    main()
