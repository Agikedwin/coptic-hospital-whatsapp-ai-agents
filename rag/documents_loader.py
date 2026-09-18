
from pathlib import Path

from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.documents import Document


# Absolute path to the docs directory
directory = Path("docs").resolve()

print(f"Documents directory: {directory}")


def get_documents() -> list[Document]:
    """
    Recursively load all supported documents from the docs directory
    using one generic loader.

    Complex metadata is filtered so that the documents can be safely
    stored in ChromaDB.
    """

    documents: list[Document] = []

    folder = directory

    if not folder.exists():
        raise FileNotFoundError(
            f"Directory '{directory}' does not exist."
        )

    supported_extensions = {
        ".pdf",
        ".docx",
        ".doc",
        ".xlsx",
        ".xls",
        ".csv",
        ".txt",
        ".md",
        ".pptx",
        ".ppt",
        ".html",
    }

    files = [
        file
        for file in folder.rglob("*")
        if file.is_file()
        and file.suffix.lower() in supported_extensions
    ]

    print(f"Found {len(files)} supported documents")

    for file in files:
        try:
            print(f"Loading: {file}")

            loader = UnstructuredFileLoader(
                str(file),
                mode="elements"
            )

            loaded_docs = loader.load()

            # Add simple metadata that Chroma supports
            for doc in loaded_docs:
                doc.metadata.update({
                    "file_name": file.name,
                    "file_type": file.suffix.lower(),
                    "source": str(file),
                })

            documents.extend(loaded_docs)

        except Exception as e:
            print(f"Failed to load {file}: {e}")

    # IMPORTANT:
    # Remove nested dictionaries and other complex metadata
    # that ChromaDB cannot store.
    documents = filter_complex_metadata(documents)

    print(f"Loaded {len(documents)} document elements")

    return documents

