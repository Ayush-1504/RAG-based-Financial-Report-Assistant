from dotenv import load_dotenv
import os

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

from langchain_community.vectorstores import FAISS

# -------------------------
# Load Environment
# -------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

# -------------------------
# LLM
# -------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=api_key
)

# -------------------------
# Embedding Model
# -------------------------
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)

# -------------------------
# Load Vector DB
# -------------------------
vector_store = FAISS.load_local(
    "faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

# -------------------------
# User Question
# -------------------------
query = input("Ask a Question: ")

# -------------------------
# Retrieve Documents
# -------------------------
docs = retriever.invoke(query)

# -------------------------
# Build Context
# -------------------------
context = "\n\n".join([doc.page_content for doc in docs])

# -------------------------
# Prompt
# -------------------------
prompt = f"""
You are an AI Financial Assistant.

Answer ONLY from the given context.

If the answer is not available,
reply:
"I could not find this information in the uploaded report."

Context:

{context}

Question:

{query}
"""

# -------------------------
# Generate Answer
# -------------------------
response = llm.invoke(prompt)

print("\n")
print("=" * 60)
print("ANSWER")
print("=" * 60)

if isinstance(response.content, list):
    print(response.content[0]["text"])
else:
    print(response.content)