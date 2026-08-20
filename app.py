import os
import shutil
import streamlit as st

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

from utils.vector_store import create_vector_store
from utils.embeddings import get_embedding_model


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()


def get_api_key():
    """Get Gemini API key from local .env or Streamlit secrets."""

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GOOGLE_API_KEY"]
        except Exception:
            api_key = None

    return api_key


API_KEY = get_api_key()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Financial Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Main App ---------- */

    .stApp {
        background-color: #f7f8fc;
    }

    /* ---------- Header ---------- */

    .hero {
        padding: 25px 30px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #111827 0%,
            #1f2937 100%
        );
        color: white;
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #d1d5db;
        margin-top: 0px;
    }

    /* ---------- Cards ---------- */

    .info-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
    }

    .answer-card {
        background: white;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.04);
        margin-top: 10px;
    }

    .source-card {
        background: #ffffff;
        padding: 13px 16px;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        margin-bottom: 8px;
        font-size: 14px;
    }

    /* ---------- Section Titles ---------- */

    .section-title {
        font-size: 22px;
        font-weight: 650;
        margin-top: 15px;
        margin-bottom: 10px;
        color: #111827;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    .sidebar-title {
        font-size: 22px;
        font-weight: 700;
        color: #111827;
    }

    .sidebar-text {
        font-size: 14px;
        color: #6b7280;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 45px;
    }

    /* ---------- Text Input ---------- */

    div[data-baseweb="input"] {
        border-radius: 10px;
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        margin-top: 40px;
        padding-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "processed" not in st.session_state:
    st.session_state.processed = False

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "questions" not in st.session_state:
    st.session_state.questions = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📄 Financial Report</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-text">'
        'Upload a financial report to start analyzing it.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Annual Report",
        type=["pdf"],
        help="Upload a PDF financial or annual report."
    )

    if uploaded_file:

        st.success("PDF uploaded")

        st.caption(
            f"📎 {uploaded_file.name}"
        )

        st.caption(
            f"📦 {uploaded_file.size / 1024 / 1024:.2f} MB"
        )

        st.divider()

        process_button = st.button(
            "⚡ Process Report",
            use_container_width=True
        )

        if process_button:

            os.makedirs("data", exist_ok=True)

            pdf_path = os.path.join(
                "data",
                uploaded_file.name
            )

            with open(pdf_path, "wb") as f:
                shutil.copyfileobj(
                    uploaded_file,
                    f
                )

            with st.spinner(
                "Processing report and building vector database..."
            ):

                try:

                    create_vector_store(
                        pdf_path
                    )

                    st.session_state.processed = True
                    st.session_state.file_name = uploaded_file.name

                    st.success(
                        "Report processed successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"Processing failed: {e}"
                    )

    else:

        st.info(
            "Upload a PDF to begin."
        )

    st.divider()

    st.markdown(
        "**How it works**"
    )

    st.markdown(
        """
        1. 📄 Upload PDF  
        2. ✂️ Split document  
        3. 🧠 Create embeddings  
        4. 🔎 Search with FAISS  
        5. 🤖 Generate answer with Gemini
        """
    )

    st.divider()

    st.caption(
        "Built with Python • LangChain • FAISS • Gemini • Streamlit"
    )


# ============================================================
# MAIN HERO
# ============================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-title">
        💰 AI Financial Assistant
    </div>
    <div class="hero-subtitle">
        Ask questions about financial reports using
        Retrieval-Augmented Generation (RAG).
    </div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# STATUS CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
        <div class="info-card">
            <b>📄 Document</b><br>
            <span style="color:#6b7280;">
            Financial Report
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
        <div class="info-card">
            <b>🧠 Retrieval</b><br>
            <span style="color:#6b7280;">
            FAISS Semantic Search
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        """
        <div class="info-card">
            <b>🤖 Generation</b><br>
            <span style="color:#6b7280;">
            Google Gemini
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CURRENT DOCUMENT STATUS
# ============================================================

if st.session_state.processed:

    st.success(
        f"✅ Ready to answer questions from "
        f"**{st.session_state.file_name}**"
    )

else:

    st.info(
        "👈 Upload a financial report from the sidebar "
        "and click **Process Report**."
    )


# ============================================================
# QUESTION AREA
# ============================================================

st.markdown(
    '<div class="section-title">💬 Ask Questions About the Report</div>',
    unsafe_allow_html=True
)

question = st.text_input(
    "Question",
    placeholder="e.g. What was Apple's total net sales in 2025?",
    label_visibility="collapsed"
)


ask_button = st.button(
    "🤖 Ask Question",
    type="primary",
    use_container_width=True
)


# ============================================================
# ASK QUESTION
# ============================================================

if ask_button:

    if not question.strip():

        st.warning(
            "Please enter a question first."
        )

    elif not os.path.exists("faiss_index"):

        st.warning(
            "Please upload and process a report first."
        )

    elif not API_KEY:

        st.error(
            "GOOGLE_API_KEY is not configured."
        )

    else:

        try:

            with st.spinner(
                "🔎 Searching the report..."
            ):

                # ------------------------------------------------
                # Load local embedding model
                # ------------------------------------------------

                embedding_model = (
                    get_embedding_model()
                )

                # ------------------------------------------------
                # Load FAISS
                # ------------------------------------------------

                vector_store = FAISS.load_local(
                    "faiss_index",
                    embedding_model,
                    allow_dangerous_deserialization=True
                )

                # ------------------------------------------------
                # Retriever
                # ------------------------------------------------

                retriever = vector_store.as_retriever(
                    search_kwargs={
                        "k": 4
                    }
                )

                # ------------------------------------------------
                # Retrieve relevant chunks
                # ------------------------------------------------

                docs = retriever.invoke(
                    question
                )

                # ------------------------------------------------
                # Build context
                # ------------------------------------------------

                context = "\n\n".join(
                    doc.page_content
                    for doc in docs
                )

            with st.spinner(
                "🤖 Generating answer..."
            ):

                # ------------------------------------------------
                # Gemini
                # ------------------------------------------------

                llm = ChatGoogleGenerativeAI(
                    model="gemini-3.6-flash",
                    google_api_key=API_KEY,
                    temperature=0
                )

                # ------------------------------------------------
                # Prompt
                # ------------------------------------------------

                prompt = f"""
You are an AI Financial Report Assistant.

Answer the user's question using ONLY the
information contained in the provided context.

Do not use outside knowledge.

If the answer cannot be found in the context,
say:

"I could not find this information in the uploaded report."

Give a clear, concise and professional answer.

Context:
{context}

Question:
{question}
"""

                response = llm.invoke(
                    prompt
                )

            # ------------------------------------------------
            # Save question
            # ------------------------------------------------

            if question not in st.session_state.questions:

                st.session_state.questions.insert(
                    0,
                    question
                )

            # Keep last 5
            st.session_state.questions = (
                st.session_state.questions[:5]
            )

            # ------------------------------------------------
            # Answer
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">💡 Answer</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="answer-card">',
                unsafe_allow_html=True
            )

            if isinstance(
                response.content,
                list
            ):

                for item in response.content:

                    if (
                        isinstance(item, dict)
                        and item.get("type") == "text"
                    ):

                        st.markdown(
                            item["text"]
                        )

            else:

                st.markdown(
                    response.content
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            # ------------------------------------------------
            # Sources
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">📚 Sources</div>',
                unsafe_allow_html=True
            )

            for i, doc in enumerate(
                docs,
                start=1
            ):

                page = doc.metadata.get(
                    "page",
                    "Unknown"
                )

                if isinstance(page, int):

                    page = page + 1

                st.markdown(
                    f"""
                    <div class="source-card">
                        📄 <b>Source {i}</b>
                        &nbsp;&nbsp;|&nbsp;&nbsp;
                        Page <b>{page}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:

            st.error(
                f"❌ Something went wrong: {e}"
            )


# ============================================================
# RECENT QUESTIONS
# ============================================================

if st.session_state.questions:

    st.divider()

    st.markdown(
        '<div class="section-title">🕘 Recent Questions</div>',
        unsafe_allow_html=True
    )

    for q in st.session_state.questions:

        st.markdown(
            f"""
            <div class="source-card">
                💬 {q}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        AI Financial Assistant • RAG-based Financial Report Analysis
    </div>
    """,
    unsafe_allow_html=True
)