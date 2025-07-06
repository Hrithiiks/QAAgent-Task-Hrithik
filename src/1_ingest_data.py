import os
import whisper
# Import the yt_dlp library
import yt_dlp

# --- Configuration ---
# Make sure to put the real YouTube URL here!
YOUTUBE_URL = "https://www.youtube.com/watch?v=IK62Rk47aas"
DATA_DIR = os.path.join("..", "data")
VIDEO_PATH = os.path.join(DATA_DIR, "video.mp4")
TRANSCRIPT_PATH = os.path.join(DATA_DIR, "transcript.txt")

def download_video():
    """Downloads a video from YouTube using the yt-dlp library."""
    print(f"Downloading video from {YOUTUBE_URL}...")
    
    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # yt-dlp options
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': VIDEO_PATH, # Specify the output path and filename
    }

    # Use the library directly
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([YOUTUBE_URL])
        
    print(f"Video downloaded to {VIDEO_PATH}")

def transcribe_video():
    """Transcribes the downloaded video using Whisper."""
    if not os.path.exists(VIDEO_PATH):
        print("Video file not found. Please download it first.")
        return

    print("Loading Whisper model...")
    # Using the 'base' model for speed. For higher accuracy, consider 'medium' or 'large'.
    model = whisper.load_model("base")

    print("Transcribing video... This may take a while.")
    result = model.transcribe(VIDEO_PATH)
    
    with open(TRANSCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(result["text"])
    
    print(f"Transcription complete. Saved to {TRANSCRIPT_PATH}")

if __name__ == "__main__":
    if not os.path.exists(VIDEO_PATH):
        download_video()
    else:
        print("Video already exists. Skipping download.")
    
    if not os.path.exists(TRANSCRIPT_PATH):
        transcribe_video()
    else:
        print("Transcript already exists. Skipping transcription.")
