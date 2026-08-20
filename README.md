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