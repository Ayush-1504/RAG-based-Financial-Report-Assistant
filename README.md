# 💰 RAG-based Financial Report Analysis Assistant

An AI-powered financial report analysis application that allows users to upload annual reports in PDF format and ask natural-language questions about the report.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from the uploaded document and generate grounded answers using Google Gemini.

## 🚀 Live Demo

[Open the Live Application](https://ayush-1504-rag-based-financial-report-assistant-app-myad05.streamlit.app/)

## 📌 Features

- 📄 Upload financial annual reports in PDF format
- ✂️ Automatically split documents into meaningful text chunks
- 🔎 Semantic search using FAISS vector database
- 🤗 Local Hugging Face embedding model
- 🤖 Google Gemini for answer generation
- 📚 Displays relevant source pages for generated answers
- 💬 Natural-language question answering
- 🎨 Interactive Streamlit interface

## 🏗️ Architecture

```text
PDF Report
    ↓
PDF Loader
    ↓
Text Splitting
    ↓
Hugging Face Embeddings
    ↓
FAISS Vector Store
    ↓
Semantic Retrieval
    ↓
Relevant Context
    ↓
Google Gemini
    ↓
AI-generated Answer + Sources

🛠️ Tech Stack
Python
Streamlit
LangChain
FAISS
Hugging Face
Google Gemini
PyPDF
📂 Project Structure
AI-Financial-Assistant/
│
├── app.py
├── requirements.txt
├── test_gemini.py
├── .gitignore
│
├── utils/
│   ├── embeddings.py
│   ├── pdf_loader.py
│   ├── rag_chain.py
│   ├── retriever.py
│   ├── text_splitter.py
│   └── vector_store.py
│
└── README.md
⚙️ How It Works
User uploads a financial report in PDF format.
The PDF is loaded and split into smaller text chunks.
Hugging Face embeddings convert the chunks into vectors.
FAISS stores the vectors and retrieves relevant information.
Google Gemini generates an answer using the retrieved context.
The application displays the answer along with source pages.
💡 Example Questions
What was Apple's total net sales in 2025?


What products does Apple sell?


What are Apple's major risk factors?


What were Apple's revenues in different segments?
💻 Run Locally
git clone https://github.com/Ayush-1504/RAG-based-Financial-Report-Assistant.git


cd RAG-based-Financial-Report-Assistant


python -m venv venv


venv\Scripts\activate


pip install -r requirements.txt


streamlit run app.py
🔐 API Configuration

Create a .env file:

GOOGLE_API_KEY=your_google_api_key

Never upload your API key to GitHub.

👨‍💻 Author

Ayush Sharma

B.Tech Computer Science & Engineering
Kalinga Institute of Industrial Technology

GitHub
