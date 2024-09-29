import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # OpenAI API configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-3.5-turbo"

    # Streamlit configuration
    STREAMLIT_PAGE_TITLE = "AI Powered Teaching Assistant"
    STREAMLIT_LAYOUT = "wide"

    # File upload configuration
    ALLOWED_EXTENSIONS = ["mp3", "mp4", "m4a", "wav", "webm", "mpeg", "mpga"]

    # YouTube API configuration (if needed in the future)
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

    # Temporary file paths
    TEMP_VIDEO_PATH = "temp_video.mp4"
    TEMP_AUDIO_PATH = "temp_audio.wav"

    # Quiz configuration
    MIN_QUIZ_QUESTIONS = 10
    MAX_QUIZ_QUESTIONS = 15

    @staticmethod
    def get_openai_api_key():
        api_key = Config.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OpenAI API key is not set. Please check your .env file.")
        return api_key

    @staticmethod
    def get_youtube_api_key():
        api_key = Config.YOUTUBE_API_KEY
        if not api_key:
            raise ValueError("YouTube API key is not set. Please check your .env file.")
        return api_key