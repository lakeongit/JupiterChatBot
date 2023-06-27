# Jupiter - AI Chatbot

Jupiter is a powerful AI chatbot built using Python, Streamlit, SQLite, and OpenAI's GPT-3. It also leverages the Wikipedia API to provide real-time information.

## Features

- Engages in conversation using GPT-3, one of the most powerful language models available.
- Remembers the last 25 messages in a conversation to maintain context.
- Fetches real-time data from Wikipedia to provide up-to-date information.

## Installation

1. Clone the repository
   git clone https://github.com/lakeongit/jupiter-chatbot.git

2. Change into the project directory
   cd jupiter-chatbot

3. Install the required Python packages
   pip install -r requirements.txt

4. Add your OpenAI API key to a new `.env` file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   Replace `your_api_key_here` with your actual OpenAI API key.

## Usage

1. Start the Streamlit app
   streamlit run app.py

2. Visit the app in your web browser at `http://localhost:8501

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
