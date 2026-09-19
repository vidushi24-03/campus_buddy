from flask import Flask, request
import sqlite3

#brings in the flask tool that gives you the tools to actually create a web application 
#request is flask's way of giving you access to whatever the user sent

app = Flask(__name__)
#creates your web app, every flask projects starts with this line

def find_answer(user_message):
        user_message = user_message.lower()

        connection = sqlite3.connect("freshers.db")
        cursor = connection.cursor()
        cursor.execute("SELECT keywords, answer FROM faq")
        all_rows = cursor.fetchall()
        connection.close()

        for row in all_rows:
                keywords = row[0]
                answer = row[1]
                keyword_list = keywords.split(" ")

                for keyword in keyword_list:
                        if keyword in user_message:
                                return answer

        return "Sorry, I don't have information on that yet."
#opens the database, gets every row from the faq table, then checks
#each row's keywords against what the user typed. Returns the first match.

@app.route("/")
#this is called a decorator. / means homepage. this tells flask that when someone visits homepage (/), run the function below

def home():
	return '''
		<h1>Southampton Freshers Bot</h1>
		<form action="/chat" method="get">
		<input type="text" name="message" placeholder="Ask a question">
		<button type="submit">Send</button>
		</form>
		'''
##creates a form
#action="/chat" says "when submitted, go to /chat". method="get" says "send the data as a query parameter in the URL.
#<input type="text" name="message"> — a text box. The name="message" is important: it decides what key the value gets stored 
#under, which is exactly the message key you're already reading with request.args.get("message").
#the button that submits the form

@app.route("/chat")
#a second page, at the address /chat
def chat():
	user_message = request.args.get("message")
	answer = find_answer(user_message)
	return answer

#reads the message the user typed, passes it to find_answer(), and returns whatever it finds

app.run(debug=True)
#this starts the server, debug=True means it auto-restarts when you save changes

