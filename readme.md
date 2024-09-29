# AI-Powered Teaching Assistant

## Overview

The AI-Powered Teaching Assistant is a Streamlit-based web application that leverages artificial intelligence to transform educational content. It allows users to upload audio/video files or provide YouTube URLs, and then generates transcripts, study notes, and interactive quizzes based on the content.

## Features

- **Transcript Generation**: Automatically transcribes audio from uploaded files or YouTube videos.
- **Notes Generation**: Creates concise, informative notes from the transcribed content.
- **Quiz Creation**: Generates an interactive quiz based on the content.
- **Multiple Input Options**: Supports both file uploads and YouTube URL inputs.
- **Interactive UI**: User-friendly interface built with Streamlit.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- pip (Python package manager)
- An OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/ai-powered-teaching-assistant.git
   cd ai-powered-teaching-assistant
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root directory
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL displayed in the terminal (usually `http://localhost:8501`).

3. Choose your input method (file upload or YouTube URL).

4. Process the video/audio to generate a transcript.

5. Click "Generate Notes and Quiz" to create study materials.

6. Take the interactive quiz and view your results.

## Project Structure

- `app.py`: Main application file
- `models.py`: Contains the Model class for API interactions
- `prompt.py`: Defines prompts for the AI model
- `config.py`: Configuration settings
- `content_generator.py`: Functions for generating notes and quizzes

## Contributing

Contributions to the AI-Powered Teaching Assistant are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- OpenAI for providing the API used in this project
- Streamlit for the wonderful web app framework
- All contributors who have helped to enhance this project