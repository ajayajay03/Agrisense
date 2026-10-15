from pathlib import Path
from google import genai


def _context(query):
    chunks = []

    for file in Path("rag_docs").glob("*.txt"):
        text = file.read_text(encoding="utf-8", errors="ignore")

        if any(word.lower() in text.lower() for word in query.split()):
            chunks.append(text[:1400])

    return "\n".join(chunks)[:3500]


def ask_agriculture(question, api_key):
    context = _context(question)

    if not api_key:
        return "Gemini API key is missing. Please check your .env file."

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are a helpful agriculture assistant.
Give practical, clear and safe farming advice.

Use this local reference when relevant:
{context}

Farmer's question:
{question}
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("GEMINI ERROR:", e)
        return "Gemini request failed. Check the VS Code terminal."