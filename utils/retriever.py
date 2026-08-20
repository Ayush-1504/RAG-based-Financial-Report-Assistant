from dotenv import load_dotenv
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# -------------------------
# Load API Key
# -------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

# -------------------------
# Load Embedding Model
# -------------------------
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)

# -------------------------
# Load FAISS Database
# -------------------------
vector_store = FAISS.load_local(
    "faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True
)

# -------------------------
# Create Retriever
# -------------------------
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

# -------------------------
# User Query
# -------------------------
query = "What was Apple's total revenue in 2025?"

# -------------------------
# Retrieve Documents
# -------------------------
results = retriever.invoke(query)

print("=" * 60)
print(f"Retrieved {len(results)} Chunks")
print("=" * 60)

for i, doc in enumerate(results, start=1):
    print(f"\nChunk {i}")
    print("-" * 60)
    print(doc.page_content[:700])
    print("\nMetadata:")
    print(doc.metadata)