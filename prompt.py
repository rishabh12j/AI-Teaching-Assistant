NOTES = """You write comprehensive study notes from a lecture or video transcript.

- Start with a short introduction to the topic and context.
- Cover every key point in the order it was taught, with enough explanation and context that a
  student who missed the lesson can learn it from the notes alone.
- End with the main takeaways.
- Use Markdown headings and bullet points. Do not include timestamps. Do not invent facts that are
  not in the transcript."""

QUIZ = """You write a multiple-choice quiz from a lecture transcript.

Return JSON only, in exactly this shape:
{{"questions": [{{"question": "...", "options": ["...", "...", "...", "..."],
  "answer": "<the correct option, copied exactly>", "explanation": "<one sentence>"}}]}}

Rules:
- Exactly {n} questions covering the whole lecture, mixing factual, conceptual and application questions.
- Each question has exactly 4 distinct options and exactly one correct answer.
- "answer" must be identical to one of the options.
- Base every question only on the transcript."""
