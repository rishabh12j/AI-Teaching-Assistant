import os


class Config:
    PAGE_TITLE = "AI-Powered Teaching Assistant"
    BASE_URL = "https://api.groq.com/openai/v1"
    TEXT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    STT_MODEL = os.getenv("GROQ_STT_MODEL", "whisper-large-v3-turbo")
    ALLOWED_EXTENSIONS = ["mp3", "mp4", "m4a", "wav", "webm", "mpeg", "mpga", "ogg", "flac"]
    MAX_UPLOAD_BYTES = 25_000_000
    MAX_TRANSCRIPT_CHARS = 24_000
    QUIZ_QUESTIONS = 10

    @staticmethod
    def api_key() -> str | None:
        # GROQ_API_KEY is preferred; OPENAI_API_KEY is accepted for older settings
        return os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
