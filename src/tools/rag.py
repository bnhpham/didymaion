from pathlib import Path
from src.config import OLLAMA_BASE_URL

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


DOCUMENT_DIR = Path("src/data/documents")
CHROMA_DIR = "src/data/chroma_db"

# Embedding model for generating vector embeddings of local documents
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)


# Load local documents
# Support only pdf, txt, and md. Can be extended to other file formats.
def load_documents():
    documents = []

    for path in DOCUMENT_DIR.glob("*"):
        if path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
            documents.extend(loader.load())
        elif path.suffix.lower() in [".txt", ".md"]:
            loader = TextLoader(str(path), encoding="utf-8")
            documents.extend(loader.load())

    return documents


# Build ChromaDB vector database
def build_vector_store():
    documents = load_documents()

    # Splitter splits document into chunks of 800 characters
    # Consecutive chunks overlap by 120 characters
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        )

    chunks = splitter.split_documents(documents)
    
    # Create embeddings for all chunks and store them in a vector database
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        )

    return vector_store


# Load vector database that contains the embeddings of all document chunks
def get_vector_store():
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
        )


# Convert the user's query into an embedding
# Retrieve the top k most semantically similar chunks from the vector database
def retrieve_internal_context(query: str, k: int = 4) -> str:
    vector_store = get_vector_store()
    docs = vector_store.similarity_search(query, k=k)

    formatted = []

    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "unknown")

        formatted.append(
            f"[Internal Document {i}]\n"
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{doc.page_content}"
            )

    return "\n\n".join(formatted)