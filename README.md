# 🥐 Croissant AI

Using [Mistral](https://mistral.ai/) and [LangChain](https://www.langchain.com/) to create a chatbot that can answer questions from La Boulangerie's wiki and docs.

## 🛠️ Setup

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Add .env file with the following variables:

```
MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY
WIKI_URL=YOUR_WIKI_URL (e.g. https://laboulangerie.fandom.com/fr/)
```

4. Run the server with `uvicorn src.app:app --reload`
