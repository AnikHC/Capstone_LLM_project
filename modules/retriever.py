from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="db",
    embedding_function=embedding
)

def query_db(query: str, k: int = 5):
    return db.similarity_search(query, k=k)