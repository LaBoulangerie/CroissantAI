# coding=utf-8

from langchain_mistralai import MistralAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import requests
from langchain_community.vectorstores import FAISS
from bs4 import BeautifulSoup

from dotenv import load_dotenv
from os import getenv

load_dotenv()

url = getenv("WIKI_URL")
api_key = getenv("MISTRAL_API_KEY")

params = {
    "action": "query",
    "format": "json",
    "list": "allpages",
    "aplimit": 1000,
    "apfrom": "",
}

page_param = {
    "action": "parse",
    "format": "json",
    "prop": "text",
}

embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=api_key)

vector = []
text_splitter = RecursiveCharacterTextSplitter()

response = requests.get(url + "/api.php", params=params)
data = response.json()
pages = data["query"]["allpages"]

for page in pages:
    title = page["title"]

    print(f"Processing page: {title}")

    page_param["page"] = title
    response = requests.get(url + "/api.php", params=page_param)
    data = response.json()

    text = data["parse"]["text"]["*"]
    soup = BeautifulSoup(text, "html.parser")
    parsed_text = soup.text.replace("\n", " ")

    doc = Document(page_content=parsed_text)
    docs = text_splitter.split_documents([doc])
    vector.extend(docs)

index = FAISS.from_documents(vector, embeddings)
index.save_local("faiss.index")
