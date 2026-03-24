# Automated Reddit-to-Shorts Video Generator

An automated Python pipeline that generates TikTok/YouTube Shorts style videos by scraping Reddit stories, converting them to TTS audio, and compositing them over background footage.

## Features
- 🤖 **No API Keys Needed for Reddit**: Scrapes public Reddit JSON data directly.
- 🎙️ **High-Quality TTS**: Uses `edge-tts` for natural-sounding voiceovers.
- 🎬 **Automated Editing**: Uses `moviepy` and `Pillow` to automatically trim background videos and render synchronized subtitle chunks.
- 🚀 **YouTube Upload Integration**: Optionally uploads the final `final_short.mp4` directly to YouTube as a public Short.

## Setup
1. Ensure you have Python 3 installed.
2. Install requirements using `pip install -r requirements.txt` (or manually install `praw`, `moviepy==1.0.3`, `edge-tts`, `Pillow<10.0.0`, `google-api-python-client`, `google-auth-oauthlib`).
3. Place a background video named `background.mp4` in the root directory.
4. (Optional) For YouTube upload, obtain a `client_secret.json` from Google Cloud Console.
5. Run `python main.py` or `.bat` helper.

## License
This project is licensed under the MIT License.
