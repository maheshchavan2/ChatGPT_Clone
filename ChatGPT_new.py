from flask import Flask, render_template, request
import os
import openai

app = Flask(__name__)

def init_api():
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")

def save_history_to_file(history):
    with open("history.txt", "w+") as f:
        f.write(history)

def load_history_from_file():
    with open("history.txt", "r") as f:
        return f.read()

def get_relevant_history(history):
    history_list = history.split(separator)
    if len(history_list) > 2:
        return separator.join(history_list[-2:])
    else:
        return history        

init_api()

initial_prompt = """You: Hi there!
You: Hello!
AI: How are you?
You: {}
AI: """

history = ""
relevant_history = ""
separator = "#####"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    global history
    prompt = request.form["text"]
    relevant_history = get_relevant_history(load_history_from_file())

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=initial_prompt.format(relevant_history + prompt),
        temperature=1,
        max_tokens=1040,
        stop=[" You:", " AI:"],
    )

    response_text = response.choices[0].text
    history += "\nYou: "+ prompt + "\n" + "AI: " + response_text + "\n" + separator
    save_history_to_file(history)

    return response_text

if __name__ == "__main__":
    app.run(debug=True)
