from langchain_community.document_loaders import TextLoader
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

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
model = ChatMistralAI(mistral_api_key=api_key, temperature=0.9)

# Define prompt template
prompt = ChatPromptTemplate.from_template(
    """Répond aux questions suivantes en utilisant uniquement le contexte fourni et la personnalité définie.

<personality>
Je suis un gentleman distingué et je parle avec élégance. Je commence toujours mes phrases par "Mesdames et Messieurs" et je termine par "Je vous remercie".
</personality>

<context>
{context}
</context>

Question: {input}"""
)

# Create a retrieval chain to answer questions
document_chain = create_stuff_documents_chain(model, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)
response = retrieval_chain.invoke({"input": input()})
print(response["answer"])
