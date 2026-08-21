# 💰 RAG-based Financial Report Analysis Assistant

An AI-powered financial report analysis application that allows users to upload annual reports in PDF format and ask natural-language questions about the report.

## 🚀 Live Demo

[Open Live Application](https://ayush-1504-rag-based-financial-report-assistant-app-myad05.streamlit.app/)

## ✨ Features

- 📄 Upload annual financial reports in PDF format
- ✂️ Automatic PDF text extraction and chunking
- 🤗 Hugging Face embeddings
- 🔎 FAISS semantic search
- 🤖 Google Gemini for answer generation
- 📚 Source page references
- 💬 Natural-language question answering
- 🎨 Streamlit web interface

## 🏗️ RAG Architecture

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
Answer + Sources
```

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- FAISS
- Hugging Face
- Google Gemini
- PyPDF

## 📂 Project Structure

```text
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
```

## ⚙️ How It Works

1. User uploads a financial report in PDF format.
2. The PDF is loaded and split into smaller text chunks.
3. Hugging Face embeddings convert the chunks into vectors.
4. FAISS stores the vectors and retrieves relevant information.
5. Google Gemini generates an answer using the retrieved context.
6. The application displays the answer along with source pages.

## 💡 Example Questions

```text
What was Apple's total net sales in 2025?

What products does Apple sell?

What are Apple's major risk factors?

What were Apple's revenues in different segments?
```

## 💻 Run Locally

Clone the repository:

```bash
git clone https://github.com/Ayush-1504/RAG-based-Financial-Report-Assistant.git
```

Navigate to the project:

```bash
cd RAG-based-Financial-Report-Assistant
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## 🔐 API Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
```

Never upload your API key to GitHub.

For Streamlit Cloud deployment, add the API key through the application's Secrets settings.

## 👨‍💻 Author

**Ayush Sharma**

B.Tech Computer Science & Engineering  
Kalinga Institute of Industrial Technology

[GitHub](https://github.com/Ayush-1504)
