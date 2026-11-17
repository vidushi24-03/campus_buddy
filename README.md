# Campus Buddy

A chatbot that answers common questions from new students (freshers) at the University of Southampton about buses, the library, catering, accommodation and more.

## How it works

Campus Buddy uses **retrieval-augmented generation (RAG)**:

1. **Retrieve:** the question is split into words and each FAQ in a SQLite database is scored by how many of its keywords match. The best few answers are picked.
2. **Generate:** those answers are sent to Google's **Gemini** model with the question. Gemini is told to answer *only* from those facts, so it replies naturally without making things up.
3. **Fallback:** if Gemini isn't set up or the request fails, the bot returns the best database answer directly, so it keeps working.

## Tech stack

- Python, Flask (web app)
- SQLite (FAQ knowledge base)
- Google Gemini API via the `google-genai` SDK

## Running it

```bash
pip install -r requirements.txt
python setup_db.py          # creates/refreshes freshers.db
cp .env.example .env        # then paste your Gemini API key into .env
python app.py
```

Open http://127.0.0.1:5000 and ask something like "Is the bus free?".

Get a free API key from [Google AI Studio](https://aistudio.google.com/). The `.env` file is in `.gitignore`, so the key never gets committed.

## Next steps

- Embeddings-based search so questions match by meaning, not exact words
- More FAQ entries (societies, timetables, GP registration)
- Logging unanswered questions to find gaps in the knowledge base
- Tests with pytest
