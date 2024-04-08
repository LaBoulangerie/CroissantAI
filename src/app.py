# coding=utf-8

from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic

from os import getenv
from dotenv import load_dotenv

load_dotenv()
api_key = getenv("MISTRAL_API_KEY")

# Define the embedding model
embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=api_key)

# Load the vector store
vector = FAISS.load_local(
    "faiss.index", embeddings, allow_dangerous_deserialization=True
)

# Define a retriever interface
retriever = vector.as_retriever()

# Define LLM
model = ChatMistralAI(mistral_api_key=api_key, temperature=0.5)

# Define prompt template
prompt = ChatPromptTemplate.from_template(
    """Répond aux questions suivantes uniquement en français en utilisant uniquement le contexte fourni.

<context>
{context}
</context>

Question de l'utilisateur : {input}"""
)

# Create a retrieval chain to answer questions
document_chain = create_stuff_documents_chain(model, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

app = FastAPI()
secret_key = getenv("SECRET_KEY", "secret")
security = HTTPBasic()


def authenticate(credentials=Depends(security)):
    if credentials.username != secret_key or credentials.password != "":
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/ask", dependencies=[Depends(authenticate)])
async def ask(request: str):
    try:
        response = retrieval_chain.invoke({"input": request})
        return {"answer": response["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    port = int(getenv("PORT", 8000))

    uvicorn.run(app, host="0.0.0.0", port=port)
