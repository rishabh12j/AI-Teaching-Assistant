# AI-Powered Teaching Assistant

Upload a recorded lesson or paste a YouTube link. Whisper transcribes it, an LLM writes structured study notes, and you take an interactive multiple-choice quiz that is scored with explanations.

**Live demo:** https://huggingface.co/spaces/Rishabh12j/Teaching_Assistant_AI

## History
- **2024:** first version on the OpenAI API (Whisper and GPT) with yt-dlp for YouTube audio.
- **2026:** rebuilt on Groq's OpenAI-compatible API, captions fetched with youtube-transcript-api instead of downloading audio, quiz output validated before it is shown, and packaged as a Docker Space.

## How it works
- **Speech-to-text:** Groq Whisper through Groq's OpenAI-compatible API.
- **Notes:** one LLM call with a structured note-taking prompt.
- **Quiz:** the LLM must return JSON (`question`, four `options`, `answer`, `explanation`). The app validates it (exactly four distinct options, answer must match one) and drops anything malformed before showing it.
- **State:** Streamlit session state keeps the transcript, notes, quiz and answers between reruns.

## Project structure
| File | Purpose |
|---|---|
| `app.py` | Streamlit interface |
| `config.py` | Model names and API settings, read from environment variables |
| `models.py` | OpenAI client pointed at Groq: chat and transcription calls |
| `prompt.py` | Prompts for notes and quiz |
| `content_generator.py` | Builds notes and quizzes, validates quiz JSON |
| `Dockerfile` | Container used by the Hugging Face Space |

## Run locally
```bash
git clone https://github.com/rishabh12j/ai-teaching-assistant.git
cd ai-teaching-assistant
pip install -r requirements.txt
export GROQ_API_KEY=your_groq_key
streamlit run app.py
```
Then open http://localhost:8501. The repo also includes a dev container, so it runs in GitHub Codespaces with no local setup (add `GROQ_API_KEY` as a Codespaces secret).

Or with Docker:
```bash
docker build -t teaching-assistant .
docker run -p 8501:8501 -e GROQ_API_KEY=your_groq_key teaching-assistant
```

## Configuration
| Setting | Default | Purpose |
|---|---|---|
| `GROQ_API_KEY` | (required) | Groq API key. `OPENAI_API_KEY` also works. |
| `GROQ_MODEL` | `openai/gpt-oss-120b` | Text model for notes and quiz |
| `GROQ_STT_MODEL` | `whisper-large-v3-turbo` | Speech-to-text model |

## Limits
Files up to 25 MB; transcripts trimmed to 24,000 characters. YouTube often refuses to share captions with cloud servers; upload the audio instead.

## Stack
Streamlit 1.67 · OpenAI Python SDK pointed at Groq · youtube-transcript-api

---

**Author:** Rishabh Jain, AI engineer (MSc Robotics and Embedded AI, Maynooth University)  
[More demos](https://huggingface.co/Rishabh12j) · [GitHub](https://github.com/rishabh12j) · [Portfolio](https://rishabh12j.github.io)
