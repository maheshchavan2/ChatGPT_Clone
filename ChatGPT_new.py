# Import necessary modules
from flask import Flask, render_template, request
import os
import openai

# Create an instance of the Flask class
app = Flask(__name__)

# Define a function to initialize the OpenAI API key and organization
def init_api():
    # Read the API key and organization ID from a .env file
    with open(".env") as env:
        for line in env:
            key, value = line.strip().split("=")
            os.environ[key] = value

    # Set the API key and organization ID in the OpenAI module
    openai.api_key = os.environ.get("API_KEY")
    openai.organization = os.environ.get("ORG_ID")

# Define a function to save the conversation history to a file
def save_history_to_file(history):
    with open("history.txt", "w+") as f:
        f.write(history)

# Define a function to load the conversation history from a file
def load_history_from_file():
    with open("history.txt", "r") as f:
        return f.read()

# Define a function to get the relevant part of the conversation history
def get_relevant_history(history):
    # Split the conversation history into a list of lines
    history_list = history.split(separator)
    # If there are more than two lines, return the last two lines
    if len(history_list) > 2:
        return separator.join(history_list[-2:])
    # Otherwise, return the entire conversation history
    else:
        return history        

# Call the init_api function to initialize the OpenAI API key and organization
init_api()

# Define the initial conversation prompt and initialize the conversation history
initial_prompt = """You: Hi there!
You: Hello!
AI: How are you?
You: {}
AI: """
history = ""
relevant_history = ""
separator = "#####"

# Define a route for the home page
@app.route("/")
def home():
    return render_template("index.html")

# Define a route for getting a response from the AI
@app.route("/get_response", methods=["POST"])
def get_response():
    # Use the global keyword to access the global history variable
    global history
    # Get the user's message from the form data
    prompt = request.form["text"]
    # Get the relevant part of the conversation history
    relevant_history = get_relevant_history(load_history_from_file())

    # Generate a response from the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=initial_prompt.format(relevant_history + prompt),
        temperature=1,
        max_tokens=1040,
        stop=[" You:", " AI:"],
    )

    # Get the text of the response from the OpenAI API
    response_text = response.choices[0].text
    # Add the user's message and the AI's response to the conversation history
    history += "\nYou: "+ prompt + "\n" + "AI: " + response_text + "\n" + separator
    # Save the updated conversation history to a file
    save_history_to_file(history)

    # Return the text of the AI's response
    return response_text

# Start the Flask web server if this file is run as the main program
if __name__ == "__main__":
    app.run(debug=True)
