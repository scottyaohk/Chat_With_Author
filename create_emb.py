from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
import pickle
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os
os.environ["OPENAI_API_KEY"] = ""

name = "Marx"
fmt = "pdf"
books = f"books/{name}.{fmt}"

# Load the doc. Split into chunks.
raw_documents = PyPDFLoader(books).load()
text_splitter = TokenTextSplitter(chunk_size=600, chunk_overlap=100)
documents = text_splitter.split_documents(raw_documents)

# Calculate embeddings. Store them in a vector database.
embeddings = OpenAIEmbeddings()

vectorStore_openAI = FAISS.from_documents(documents, embeddings)

with open(f"vectordbs/{name}.pkl", "wb") as f:
    pickle.dump(vectorStore_openAI, f)
