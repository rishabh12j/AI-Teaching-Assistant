import streamlit as st
import os
from models import Model
from prompt import Prompt
from config import Config
from content_generator import generate_notes, generate_quiz
import yt_dlp
import logging
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize OpenAI client
@st.cache_resource
def init_openai_client():
    return OpenAI(api_key=Config.get_openai_api_key())

client = init_openai_client()

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(id)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return f"{info['id']}.mp3"

def get_transcript_from_file(uploaded_file):
    if uploaded_file is not None:
        with st.spinner("Transcribing... This may take a few minutes."):
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=uploaded_file
            )
        return transcript.text.strip()
    return None

def get_transcript_from_url(url):
    try:
        if url != '':
            with st.spinner("Downloading audio..."):
                mp3_file = download_audio(url)
            
            file_stats = os.stat(mp3_file)
            logging.info(f'Size of audio file in Bytes: {file_stats.st_size}')
            
            if file_stats.st_size <= 25000000:  # OpenAI has a 25MB limit
                with st.spinner("Transcribing... This may take a few minutes."):
                    with open(mp3_file, "rb") as audio_file:
                        try:
                            transcript = client.audio.transcriptions.create(
                                model="whisper-1", 
                                file=audio_file
                            )
                            result = transcript.text.strip()
                        except Exception as api_error:
                            logging.error(f"API Error: {str(api_error)}")
                            result = f"API Error: {str(api_error)}"
                
                # Clean up the downloaded file
                os.remove(mp3_file)
                
                return result
            else:
                os.remove(mp3_file)
                return "Error: The audio file is too large. Please choose a shorter video (up to ~25MB audio file size)."
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"

def display_quiz(quiz_content):
    st.subheader("Quiz")
    with st.form(key='quiz_form'):
        user_answers = {}
        for i, q in enumerate(quiz_content, 1):
            st.write(f"{i}. {q['question']}")
            user_answers[i] = st.radio(f"Question {i}", q['options'], key=f"q{i}")
            st.write("")
        
        submit_button = st.form_submit_button(label='Submit Quiz')
    
    if submit_button:
        score = calculate_score(quiz_content, user_answers)
        st.success(f"Your score: {score}/{len(quiz_content)}")
        st.session_state.quiz_submitted = True
        st.session_state.user_answers = user_answers
        st.rerun()  # Rerun to update the display

def calculate_score(quiz_content, user_answers):
    score = 0
    for i, q in enumerate(quiz_content, 1):
        if user_answers[i] == q['correct_answer']:
            score += 1
    return score

def show_quiz_results(quiz_content, user_answers):
    st.subheader("Quiz Results")
    for i, q in enumerate(quiz_content, 1):
        st.write(f"{i}. {q['question']}")
        user_choice = user_answers.get(i, "Not answered")
        correct_answer = q['correct_answer']
        
        if user_choice == correct_answer:
            st.success(f"Your answer: {user_choice} (Correct)")
        else:
            st.error(f"Your answer: {user_choice}")
            st.success(f"Correct answer: {correct_answer}")
        
        st.write("")  # Add some space between questions

def main():
    st.title("AI-Powered Teaching Assistant")

    # Initialize session state variables
    if 'transcript' not in st.session_state:
        st.session_state.transcript = None
    if 'notes' not in st.session_state:
        st.session_state.notes = None
    if 'quiz' not in st.session_state:
        st.session_state.quiz = None
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = None
    if 'input_method' not in st.session_state:
        st.session_state.input_method = "Upload File"

    # Display input method selection
    if not st.session_state.quiz_submitted:
        st.session_state.input_method = st.radio("Choose input method:", ("Upload File", "YouTube URL"))
    else:
        st.info("Quiz submitted. Refresh the page to change the input method.")
        st.radio("Input method (disabled):", ("Upload File", "YouTube URL"), disabled=True, index=0 if st.session_state.input_method == "Upload File" else 1)

    # Handle file upload or YouTube URL input
    if st.session_state.input_method == "Upload File":
        uploaded_file = st.file_uploader("Choose a file", type=Config.ALLOWED_EXTENSIONS, help="Limit 25MB per file • MP3, MP4, M4A, WAV, WEBM, MPEG, MPGA, MPG, MPEG4")
        if uploaded_file is not None:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
            st.write(file_details)
            if uploaded_file.size <= 25000000:  # 25 MB in bytes
                if st.button("Process Video"):
                    st.session_state.transcript = get_transcript_from_file(uploaded_file)
                    st.rerun()
            else:
                st.error("File size exceeds 25 MB limit. Please upload a smaller file.")
    else:
        url = st.text_input("Enter YouTube URL:")
        if url:
            if st.button("Process Video"):
                st.session_state.transcript = get_transcript_from_url(url)
                st.rerun()

    if st.session_state.transcript:
        st.subheader("Transcript")
        st.text_area("Generated Transcript", st.session_state.transcript, height=200)

        if st.button("Generate Notes and Quiz") or (st.session_state.notes and st.session_state.quiz):
            if not st.session_state.notes:
                with st.spinner("Generating notes..."):
                    st.session_state.notes = generate_notes(st.session_state.transcript)
            if not st.session_state.quiz:
                with st.spinner("Generating quiz..."):
                    st.session_state.quiz = generate_quiz(st.session_state.transcript)
            
            st.subheader("Generated Notes")
            st.markdown(st.session_state.notes)
            
            if not st.session_state.quiz_submitted:
                display_quiz(st.session_state.quiz)
            else:
                show_quiz_results(st.session_state.quiz, st.session_state.user_answers)
                st.info("Quiz already submitted. Refresh the page to take the quiz again.")

if __name__ == "__main__":
    main()