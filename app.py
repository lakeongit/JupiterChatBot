import os
import openai
import sqlite3
import requests
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Fetch the API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI API
openai.api_key = OPENAI_API_KEY

# Initialize the SQLite database
conn = sqlite3.connect('chatbot.db')
c = conn.cursor()

# Create a table to store conversation data if it doesn't already exist
c.execute('''
    CREATE TABLE IF NOT EXISTS conversations 
    (id INTEGER PRIMARY KEY, user_input TEXT, bot_output TEXT)
''')
conn.commit()

def get_wikipedia_summary(topic):
    response = requests.get(
        'https://en.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': topic,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }
    ).json()

    page = next(iter(response['query']['pages'].values()))
    return page['extract'] if 'extract' in page else None

def chat_with_bot(user_input):
    # Check if the user is asking for current information
    if "tell me about" in user_input.lower():
        topic = user_input.lower().split("tell me about", 1)[1].strip()
        info = get_wikipedia_summary(topic)

        if info:
            return info

    # Fetch the last 25 responses from the bot and user
    c.execute('SELECT user_input, bot_output FROM conversations ORDER BY id DESC LIMIT 25')
    conversation_history = c.fetchall()

    # Format the history for the prompt
    conversation_history = "\n".join([f"User: {x[0]}\nJupiter: {x[1]}" for x in conversation_history[::-1]])

    # Pass both the user_input and conversation_history to the model
    prompt = f"{conversation_history}\nUser: {user_input}\nJupiter:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=100
    )

    # Extract the model's output
    bot_output = response.choices[0].text.strip()

    # Store the conversation in the database
    c.execute('INSERT INTO conversations (user_input, bot_output) VALUES (?, ?)', (user_input, bot_output))
    conn.commit()

    return bot_output

# Streamlit application
st.title("AI Chatbot")

user_input = st.text_input("You: ", "")
if st.button("Send"):
    bot_output = chat_with_bot(user_input)
    st.markdown(f"Jupiter: {bot_output}")
