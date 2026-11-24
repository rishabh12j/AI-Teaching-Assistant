from openai import OpenAI

from config import Config


def client() -> OpenAI:
    return OpenAI(api_key=Config.api_key(), base_url=Config.BASE_URL)


def chat(system: str, user: str, *, json_mode: bool = False, max_tokens: int = 4000) -> str:
    kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
    response = client().chat.completions.create(
        model=Config.TEXT_MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0.4,
        max_tokens=max_tokens,
        **kwargs,
    )
    return response.choices[0].message.content or ""
