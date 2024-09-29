from openai import OpenAI
from config import Config

class Model:
    @staticmethod
    def openai_chatgpt(transcript, prompt, extra=""):
        client = OpenAI(api_key=Config.get_openai_api_key())
        model = Config.OPENAI_MODEL
        
        message = [{"role": "system", "content": prompt + extra},
                   {"role": "user", "content": transcript}]
        try:
            response = client.chat.completions.create(
                model=model, 
                messages=message,
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            response_error = "⚠️ There is a problem with the API key or with python module."
            return response_error, str(e)