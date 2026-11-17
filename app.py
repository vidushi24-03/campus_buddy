from flask import Flask, request
import sqlite3
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

#flask gives you the tools to create a web app, request lets you read what the user sent
#re is python's regular expressions library, used here to split the message into words
#dotenv reads your secret API key from a .env file so it never goes into your code or github
#genai is google's official library for talking to gemini

load_dotenv()
#loads GEMINI_API_KEY from the .env file. the gemini client looks for that exact name automatically

app = Flask(__name__)
#creates your web app, every flask project starts with this line

MODEL_NAME = "gemini-3.5-flash-lite"
#kept in one place so it's easy to switch to a different gemini model later

SYSTEM_INSTRUCTION = """You are Campus Buddy, a friendly helper for new students (freshers) at the University of Southampton.
Answer using ONLY the facts given to you in the message. Do not invent bus numbers, prices, times, dates or places.
If the facts don't answer the question, say you're not sure and suggest checking the University website or asking the Students' Union.
You can reply naturally to greetings and small talk. Keep answers short, warm and easy to read."""
#the system instruction tells gemini how to behave for every message.
#the most important rule is "only use the facts given", which stops it making things up (hallucinating)

try:
        client = genai.Client(http_options=types.HttpOptions(timeout=90000))
except Exception:
        client = None
#creates the connection to gemini once when the app starts.
#if there's no API key, client stays None and the bot still works using just the database


def get_words(text):
        return set(re.findall(r"[a-z]+", text.lower()))
#turns "Is the bus free?" into {"is", "the", "bus", "free"}
#matching whole words fixes the old bug where "route" matched inside "router"


def find_relevant_faqs(user_message, how_many=3):
        message_words = get_words(user_message)

        connection = sqlite3.connect("freshers.db")
        cursor = connection.cursor()
        cursor.execute("SELECT keywords, answer FROM faq")
        all_rows = cursor.fetchall()
        connection.close()

        scored_rows = []
        for keywords, answer in all_rows:
                keyword_set = set(keywords.split())
                score = len(keyword_set & message_words)
                if score > 0:
                        scored_rows.append((score, answer))

        scored_rows.sort(key=lambda row: row[0], reverse=True)
        return [answer for score, answer in scored_rows[:how_many]]
#gives every faq row a score = how many of its keywords are in the user's message
#(& means "the words in both sets"). then returns the best few answers, highest score first.
#this fixes the old bug where the FIRST row with any match won, even if a later row matched better


def ask_gemini(user_message, facts):
        if facts:
                facts_text = "\n".join("- " + fact for fact in facts)
        else:
                facts_text = "(no matching facts found in the database)"

        prompt = f"Facts:\n{facts_text}\n\nStudent's question: {user_message}"

        response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION
        ))
        return response.text
#this pattern is called retrieval-augmented generation (RAG):
#1. retrieve the relevant facts from your own database
#2. give them to gemini along with the question
#3. gemini writes a natural reply, but based on your facts


def find_answer(user_message):
        facts = find_relevant_faqs(user_message)

        if client is not None:
                try:
                        return ask_gemini(user_message, facts)
                except Exception as error:
                        print("Gemini error, falling back to database:", error)

        if facts:
                return facts[0]
        return "Sorry, I don't have information on that yet."
#tries gemini first. if gemini isn't set up or fails (no internet, rate limit, etc.)
#it falls back to the best database answer, so the bot never just breaks


@app.route("/")
#this is called a decorator. / means homepage. when someone visits the homepage, run the function below
def home():
	return '''
		<h1>Southampton Freshers Bot</h1>
		<form action="/chat" method="get">
		<input type="text" name="message" placeholder="Ask a question">
		<button type="submit">Send</button>
		</form>
		'''
#creates a form. action="/chat" says "when submitted, go to /chat"
#name="message" decides the key the text is stored under, which /chat reads with request.args.get("message")


@app.route("/chat")
#a second page, at the address /chat
def chat():
	user_message = request.args.get("message", "").strip()
	if user_message == "":
		return "Please type a question first!"
	return find_answer(user_message)
#reads the message ("" if it's missing, which fixes the old crash on an empty request),
#then passes it to find_answer() and returns the reply


if __name__ == "__main__":
	app.run(debug=True)
#only starts the server when you run "python app.py" directly (not when another file imports this one).
#debug=True auto-restarts when you save. it's for local development only, never turn it on for a real deployed site
