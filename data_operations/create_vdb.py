from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
import shutil
from langchain_openai import OpenAIEmbeddings
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
Data_Path = "E:\Ali\Professional Life\GovChatbot\cleaned text"

def load_documents():
    loader = DirectoryLoader(Data_Path, glob = "*.txt")
    documents = loader.load()
    return documents

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 500,
    length_function = len,
    add_start_index = True
)

chunks = text_splitter.split_documents(load_documents())
print(len(chunks), " is the number of the new chunks")

example_chunk = chunks[10]
print(example_chunk)

CHROMA_PATH = "chroma"

def save_db(chunks):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(api_key = OPENAI_API_KEY), persist_directory=CHROMA_PATH
    )
    
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    
save_db(chunks)
