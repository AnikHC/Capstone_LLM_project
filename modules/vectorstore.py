from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

def create_vector_db(chunks, db_path):
    embedding = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(
        documents=chunks,   # ✅ fixed
        embedding=embedding,
        persist_directory=db_path
    )

    db.persist()
    return db