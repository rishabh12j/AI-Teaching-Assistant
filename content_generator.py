from models import Model
from prompt import Prompt

def generate_notes(transcript):
    return Model.openai_chatgpt(transcript=transcript, prompt=Prompt.prompt1())

def generate_quiz(transcript):
    raw_quiz = Model.openai_chatgpt(transcript, Prompt.prompt1(ID='quiz'))
    return parse_quiz_content(raw_quiz)

def parse_quiz_content(raw_quiz):
    quiz_content = []
    questions = raw_quiz.strip().split("\n\n")

    for question in questions:
        lines = question.split("\n")
        if len(lines) < 6:  # Question + 4 options + correct answer
            continue

        question_text = lines[0].split(".", 1)[-1].strip()
        options = [line.split(")", 1)[-1].strip() for line in lines[1:5]]
        correct_answer = lines[-1].split(":")[-1].strip()

        quiz_content.append({
            "question": question_text,
            "options": options,
            "correct_answer": correct_answer
        })

    return quiz_content[:10]  # Ensure we return at most 10 questions