"""AI-Powered Teaching Assistant (Streamlit).

Upload a lesson or paste a YouTube link: Whisper transcribes it, an LLM writes study notes,
and you take a scored multiple-choice quiz. All models run on Groq through its
OpenAI-compatible API.
"""

import logging

import streamlit as st

from config import Config
from content_generator import generate_notes, generate_quiz, transcribe_file, youtube_transcript

logging.basicConfig(level=logging.INFO)
st.set_page_config(page_title=Config.PAGE_TITLE, page_icon="🎓", layout="centered")


def reset_quiz():
    st.session_state.answers = {}
    st.session_state.submitted = False


def init_state():
    defaults = {"transcript": None, "notes": None, "quiz": None, "answers": {}, "submitted": False}
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def new_transcript(text: str):
    st.session_state.transcript = text
    st.session_state.notes = None
    st.session_state.quiz = None
    reset_quiz()


def show_quiz(quiz):
    st.subheader("Quiz")
    with st.form("quiz_form"):
        for i, q in enumerate(quiz):
            st.markdown(f"**{i + 1}. {q['question']}**")
            st.session_state.answers[i] = st.radio(
                f"Answer {i + 1}", q["options"], key=f"q{i}", index=None, label_visibility="collapsed"
            )
        submitted = st.form_submit_button("Submit quiz", type="primary")
    if submitted:
        st.session_state.submitted = True
        st.rerun()


def show_results(quiz):
    score = sum(1 for i, q in enumerate(quiz) if st.session_state.answers.get(i) == q["answer"])
    st.success(f"Your score: {score} / {len(quiz)}")
    for i, q in enumerate(quiz):
        chosen = st.session_state.answers.get(i) or "Not answered"
        if chosen == q["answer"]:
            st.markdown(f"✅ **{i + 1}. {q['question']}** — {chosen}")
        else:
            st.markdown(f"❌ **{i + 1}. {q['question']}** — you chose *{chosen}*; correct: **{q['answer']}**")
        if q.get("explanation"):
            st.caption(q["explanation"])
    st.button("Try the quiz again", on_click=reset_quiz)


def main():
    init_state()
    st.title("🎓 AI-Powered Teaching Assistant")
    st.write("Turn a recorded lesson into study notes and a scored quiz.")

    if not Config.api_key():
        st.error("This Space is missing its Groq key. The owner needs to add the secret `GROQ_API_KEY`.")
        st.stop()

    method = st.radio("Input", ["Upload audio", "YouTube link"], horizontal=True)
    if method == "Upload audio":
        uploaded = st.file_uploader(
            "Audio or video file (up to 25 MB)", type=Config.ALLOWED_EXTENSIONS
        )
        if uploaded and st.button("Transcribe", type="primary"):
            if uploaded.size > Config.MAX_UPLOAD_BYTES:
                st.error("That file is over 25 MB. Please upload a shorter recording.")
            else:
                with st.spinner("Transcribing…"):
                    try:
                        new_transcript(transcribe_file(uploaded.name, uploaded.getvalue()))
                    except Exception as exc:
                        st.error(f"Transcription failed: {exc}")
    else:
        url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=…")
        if url and st.button("Get transcript", type="primary"):
            with st.spinner("Fetching captions…"):
                try:
                    new_transcript(youtube_transcript(url))
                except Exception as exc:
                    st.error(str(exc))

    if not st.session_state.transcript:
        return

    with st.expander("Transcript", expanded=False):
        st.write(st.session_state.transcript)

    if st.session_state.notes is None and st.button("Generate notes and quiz", type="primary"):
        with st.spinner("Writing notes…"):
            st.session_state.notes = generate_notes(st.session_state.transcript)
        with st.spinner("Writing quiz…"):
            st.session_state.quiz = generate_quiz(st.session_state.transcript)

    if st.session_state.notes:
        st.subheader("Study notes")
        st.markdown(st.session_state.notes)
    quiz = st.session_state.quiz
    if quiz is not None:
        if not quiz:
            st.warning("The quiz could not be generated this time. Try again.")
        elif st.session_state.submitted:
            show_results(quiz)
        else:
            show_quiz(quiz)


if __name__ == "__main__":
    main()
