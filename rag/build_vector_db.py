from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from documents_loader import get_documents


VECTOR_DB_DIR = Path("./vectorDB").resolve()
COLLECTION_NAME = "family_planning_docs"


documents = get_documents()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)


vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory=str(VECTOR_DB_DIR),
    collection_name=COLLECTION_NAME
)

print(f"Stored {len(docs)} chunks successfully.")