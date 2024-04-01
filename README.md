# 🥐🤖 Croissant AI

HTTP server that uses the Mistral API to answer question from the La Boulangerie Wiki.

Using [Langchain](https://langchain.com/) , [Mistral](https://mistral.ai) and [FastAPI](https://fastapi.tiangolo.com/).

## 🛠️ Setup

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Add .env file with the following variables:

```
MISTRAL_API_KEY=YOUR_MISTRAL_API_KEY
WIKI_URL=YOUR_WIKI_URL (e.g. https://laboulangerie.fandom.com/fr/)
SECRET_KEY=YOUR_SECRET
```

4. Run the server with `uvicorn src.app:app --reload`

## 🚀 Usage

Simple curl request to test the server:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"request": "Quelle est la capitale de Goast ?"}' \
  -u SECRET_KEY: \
  http://localhost:8000/ask
```

Should return something like "La capitale de Goast est Tharass."
