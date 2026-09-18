from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


VECTOR_DB_DIR = Path("./vectorDB").resolve()
COLLECTION_NAME = "family_planning_docs"


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)


vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(VECTOR_DB_DIR)
)


retriever = vectorstore.as_retriever(

    search_kwargs={"k": 3}
)