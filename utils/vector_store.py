from langchain_community.vectorstores import FAISS

from utils.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from utils.embeddings import get_embedding_model


def create_vector_store(pdf_path):
    """
    Create FAISS vector store from uploaded PDF.
    """

    print("=" * 60)
    print("Creating FAISS Vector Store")
    print("=" * 60)

    # Load PDF
    documents = load_pdf(pdf_path)

    print(f"Total Pages: {len(documents)}")

    # Split PDF
    chunks = split_documents(documents)

    print(f"Total Chunks Created: {len(chunks)}")

    # IMPORTANT:
    # No chunks[:50] now.
    # We are processing the complete report.

    # Local embedding model
    embedding_model = get_embedding_model()

    # Create FAISS
    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    # Save FAISS
    vector_store.save_local("faiss_index")

    print("✅ FAISS Vector Store Created Successfully!")
    print("✅ Saved in 'faiss_index' folder")

    return vector_store