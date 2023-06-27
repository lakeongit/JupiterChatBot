Jupiter - AI Chatbot

Jupiter is a powerful AI chatbot built using Python, Streamlit, SQLite, OpenAI's GPT-3, Alpha Vantage and News API. It can provide real-time information about a specific topic from Wikipedia, the latest news headlines, and stock prices.
Features

    Engages in conversation using GPT-3, one of the most powerful language models available.
    Remembers the last 25 messages in a conversation to maintain context.
    Fetches real-time data from Wikipedia to provide up-to-date information.
    Provides the latest news headlines using the News API.
    Provides real-time stock prices using the Alpha Vantage API.

Installation

    Clone the repository

git clone https://github.com/lakeongit/jupiter-chatbot.git


Change into the project directory
Install the required Python packages
pip install -r requirements.txt

Add your API keys to a new .env file

bash

    echo "OPENAI_API_KEY=your_openai_api_key" > .env
    echo "NEWS_API_KEY=your_news_api_key" >> .env
    echo "ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key" >> .env

    Replace your_openai_api_key, your_news_api_key, and your_alpha_vantage_api_key with your actual API keys.

Usage

    Start the Streamlit app

    arduino

    streamlit run app.py

    Visit the app in your web browser at http://localhost:8501

Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
