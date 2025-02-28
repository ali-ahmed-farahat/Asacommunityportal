from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API = os.getenv("OPENAI_API")
def search(query, CHROMA_PATH):
    # parser = argparse.ArgumentParser()
    # parser.add_argument(query, type=str, help="The query text.")
    # args = parser.parse_args()
    # query_text = args.query_text

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings(api_key=OPENAI_API)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query, k=3)
    if not (len(results) == 0 or results[0][1] < 0.7):
      context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
      return context_text
    
    
