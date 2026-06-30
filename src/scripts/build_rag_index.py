from src.tools.rag import build_vector_store

if __name__ == "__main__":

    # Build ChromaDB vector database containing the embeddings of all document chunks
    build_vector_store()
    print("RAG indexing completed.")