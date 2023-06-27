import os
import openai
import sqlite3
import requests
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Fetch the API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

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

def get_latest_news():
    response = requests.get(
        'https://newsapi.org/v2/top-headlines',
        params={
            'country': 'us',
            'apiKey': NEWS_API_KEY
        }
    ).json()

    articles = response.get('articles', [])
    return [article['title'] for article in articles[:5]]

def get_stock_price(symbol):
    response = requests.get(
        f'https://www.alphavantage.co/query',
        params={
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': ALPHA_VANTAGE_API_KEY
        }
    ).json()

    data = response.get('Time Series (Daily)', {})
    latest_date = max(data.keys())
    return data[latest_date]['4. close'] if data else None

def chat_with_bot(user_input):
    # Fetch the last 25 responses from the bot and user
    c.execute('SELECT user_input, bot_output FROM conversations ORDER BY id DESC LIMIT 25')
    conversation_history = c.fetchall()

    # Format the history for the prompt
    conversation_history = "\n".join([f"User: {x[0]}\nJupiter: {x[1]}" for x in conversation_history[::-1]])

    # Check if the user is asking for current information
    if "tell me about" in user_input.lower():
        topic = user_input.lower().split("tell me about", 1)[1].strip()
        info = get_wikipedia_summary(topic)

        if info:
            return info

    elif "get news" in user_input.lower():
        news = get_latest_news()

        if news:
            return "\n".join(news)

    elif "stock price of" in user_input.lower():
        symbol = user_input.lower().split("stock price of", 1)[1].strip()
        price = get_stock_price(symbol)

        if price:
            return f"The current stock price of {symbol} is {price}."

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
