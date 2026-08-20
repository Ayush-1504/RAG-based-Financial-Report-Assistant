from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):

    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    return documents


if __name__ == "__main__":

    pdf_path = "data/annual_report.pdf"

    documents = load_pdf(pdf_path)

    print("=" * 60)
    print(f"Total Pages : {len(documents)}")
    print("=" * 60)

    print("\nFirst Page Content:\n")
    print(documents[0].page_content[:1000])

    print("\nMetadata:\n")
    print(documents[0].metadata)