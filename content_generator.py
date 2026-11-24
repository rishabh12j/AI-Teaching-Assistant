import json
import logging
import re

import models
import prompt
from config import Config


def _clip(transcript: str) -> str:
    return transcript[: Config.MAX_TRANSCRIPT_CHARS]


def transcribe_file(name: str, data: bytes) -> str:
    result = models.client().audio.transcriptions.create(model=Config.STT_MODEL, file=(name, data))
    return result.text.strip()


def youtube_transcript(url: str) -> str:
    from youtube_transcript_api import YouTubeTranscriptApi

    match = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", url)
    if not match:
        raise ValueError("That does not look like a YouTube link.")
    try:
        fetched = YouTubeTranscriptApi().fetch(match.group(1), languages=["en", "en-GB", "en-US", "hi"])
    except Exception as exc:
        raise ValueError(
            "YouTube would not share captions for this video with a cloud server "
            f"({type(exc).__name__}). Download the audio and upload it instead."
        ) from exc
    return " ".join(snippet.text for snippet in fetched)


def generate_notes(transcript: str) -> str:
    try:
        return models.chat(prompt.NOTES, _clip(transcript))
    except Exception as exc:
        logging.exception("notes failed")
        return f"⚠️ Notes could not be generated ({type(exc).__name__}: {exc})."


def parse_quiz(raw: str) -> list[dict]:
    data = json.loads(raw)
    questions = []
    for item in data.get("questions", []):
        options = [str(o).strip() for o in item.get("options", [])]
        answer = str(item.get("answer", "")).strip()
        if len(options) == 4 and answer in options and item.get("question"):
            questions.append(
                {"question": str(item["question"]).strip(), "options": options, "answer": answer,
                 "explanation": str(item.get("explanation", "")).strip()}
            )
    return questions[: Config.QUIZ_QUESTIONS]


def generate_quiz(transcript: str) -> list[dict]:
    try:
        raw = models.chat(prompt.QUIZ.format(n=Config.QUIZ_QUESTIONS), _clip(transcript), json_mode=True)
        return parse_quiz(raw)
    except Exception:
        logging.exception("quiz failed")
        return []
