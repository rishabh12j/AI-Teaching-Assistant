class Prompt:
    @staticmethod
    def prompt1(ID=0):
        if ID == 0:
            prompt_text = """Your task: Generate comprehensive notes from a video transcript, highlighting key points, details, and insights. The notes should be clear, structured, and informative, making it easy for someone to understand the video's content thoroughly.

                                Guidelines:

                                Focus on key points: Identify and list all the essential aspects of the video.
                                Provide detailed insights: Expand on the key points with relevant information and context.
                                Maintain clarity and structure: Ensure the notes are well-organized and easy to follow.
                                Capture the essence of the video: Go beyond simple listings. Integrate detailed explanations and interesting insights to provide a thorough understanding.

                                Input:

                                The provided video transcript will be your content source.

                                Example (for illustration purposes only):

                                Introduction: Briefly introduce the video's topic and context.
                                Key Points and Details:
                                Point A: Describe the first crucial aspect with clarity and depth, including relevant details.
                                Point B: Elaborate on a second significant point, providing necessary explanations and context.
                                Point C: Continue listing and describing key points, ensuring each is thoroughly explained.
                                Conclusions and Insights: Summarize the main takeaways from the video, including any final thoughts or implications.

                                Additional Tips:

                                Tailor the tone: Adjust your language to match the video's intended audience and overall style.
                                Weave in storytelling elements: Use vivid descriptions and engaging transitions to make the notes more memorable.
                                Proofread carefully: Ensure your final notes are free of grammatical errors and typos.

                                By following these guidelines, you can effectively transform video transcripts into comprehensive and informative notes, providing a thorough understanding of the video's content."""

        elif ID == "quiz":
            prompt_text = """Your task: Create a comprehensive quiz based on a video lecture transcript. The quiz should consist of 10 to 15 multiple-choice questions (MCQs) that cover the key points and details presented in the lecture.

                                    Guidelines:
                                    Focus on key concepts: Each question should address a significant point or concept discussed in the lecture.
                                    Ensure clarity and accuracy: Formulate questions clearly and provide accurate options. Each question should have only one correct answer.
                                    Cover the entire lecture: Ensure the quiz questions comprehensively cover all major sections and topics discussed in the video.
                                    Answer Key: Provide the correct answer for each question.

                                    1. Create exactly 10 multiple-choice questions.
                                    2. Each question should have exactly 4 options (A, B, C, D).
                                    3. Provide the correct answer after each question.
                                    4. Use the following format for each question:

                                    1. [Question text]
                                    A. [Option A]
                                    B. [Option B]
                                    C. [Option C]
                                    D. [Option D]
                                    Correct Answer: [A/B/C/D]

                                    2. [Next question...]

                                    Additional Tips:

                                    Ensure question variety: Include a mix of factual, conceptual, and application-based questions.
                                    Use clear and concise language: Make sure questions and options are easily understood.
                                    Balance difficulty levels: Include a range of easy, moderate, and challenging questions to adequately assess the viewer's understanding.
                                    Proofread carefully: Ensure there are no grammatical errors or ambiguities in the questions and options.

                                    By following these guidelines, you can create an effective and engaging quiz that tests the viewer's comprehension of the video's content."""

        else:
            prompt_text = "NA" 

        return prompt_text