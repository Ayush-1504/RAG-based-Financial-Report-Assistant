import os
import shutil
import streamlit as st

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

from utils.vector_store import create_vector_store
from utils.embeddings import get_embedding_model


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GOOGLE API KEY
# ============================================================

# Local:
#     .env file se API key read hogi
#
# Streamlit Cloud:
#     st.secrets["GOOGLE_API_KEY"] se API key read hogi

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:

    try:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

    except Exception:
        GOOGLE_API_KEY = None


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Financial Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CHECK API KEY
# ============================================================

if not GOOGLE_API_KEY:

    st.error(
        "⚠️ GOOGLE_API_KEY is not configured."
    )

    st.info(
        "Add GOOGLE_API_KEY to your .env file "
        "for local development or Streamlit Secrets "
        "for deployment."
    )

    st.stop()


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

    st.title("📄 Financial Report")

    st.caption(
        "Upload an annual report and ask questions using AI."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Annual Report",
        type=["pdf"],
        help="Upload a financial or annual report in PDF format."
    )

    if uploaded_file is not None:

        st.success("PDF uploaded")

        st.write(
            f"**File:** {uploaded_file.name}"
        )

        file_size = uploaded_file.size / (1024 * 1024)

        st.caption(
            f"Size: {file_size:.2f} MB"
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

            try:

                with open(pdf_path, "wb") as f:

                    shutil.copyfileobj(
                        uploaded_file,
                        f
                    )

                with st.spinner(
                    "📄 Reading PDF and creating vector database..."
                ):

                    create_vector_store(
                        pdf_path
                    )

                st.session_state.processed = True

                st.session_state.file_name = (
                    uploaded_file.name
                )

                st.success(
                    "✅ Report processed successfully!"
                )

            except Exception as e:

                st.error(
                    f"❌ Processing failed: {e}"
                )


    else:

        st.info(
            "Upload a PDF to begin."
        )

    st.divider()

    st.subheader("⚙️ How it works")

    st.write(
        """
        **1.** 📄 Upload PDF

        **2.** ✂️ Split document

        **3.** 🧠 HuggingFace Embeddings

        **4.** 🔎 FAISS Semantic Search

        **5.** 🤖 Gemini generates answer
        """
    )

    st.divider()

    st.caption(
        "Python • LangChain • FAISS • Gemini • Streamlit"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title("💰 AI Financial Assistant")

st.write(
    "Analyze annual reports and ask questions using "
    "Retrieval-Augmented Generation (RAG)."
)

st.divider()


# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.subheader("📄 Financial Reports")

    st.write(
        "Upload annual reports in PDF format "
        "and process them automatically."
    )


with col2:

    st.subheader("🔎 Smart Retrieval")

    st.write(
        "FAISS searches the report and retrieves "
        "the most relevant sections."
    )


with col3:

    st.subheader("🤖 AI Answers")

    st.write(
        "Google Gemini generates answers using "
        "the retrieved report context."
    )


st.divider()


# ============================================================
# REPORT STATUS
# ============================================================

if st.session_state.processed:

    st.success(
        f"✅ Ready to analyze: "
        f"**{st.session_state.file_name}**"
    )

else:

    st.info(
        "👈 Upload a financial report from the sidebar "
        "and click **Process Report** to begin."
    )


# ============================================================
# QUESTION SECTION
# ============================================================

st.subheader(
    "💬 Ask Questions About the Report"
)

question = st.text_input(
    "Enter your question",
    placeholder=(
        "Example: What was Apple's total net sales in 2025?"
    )
)

ask_button = st.button(
    "🤖 Ask Question",
    use_container_width=True
)


# ============================================================
# ASK QUESTION
# ============================================================

if ask_button:

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    elif not os.path.exists("faiss_index"):

        st.warning(
            "Please upload and process a report first."
        )

    else:

        try:

            # =================================================
            # LOAD EMBEDDING MODEL
            # =================================================

            with st.spinner(
                "🔎 Searching the financial report..."
            ):

                embedding_model = (
                    get_embedding_model()
                )

                # =================================================
                # LOAD FAISS
                # =================================================

                vector_store = FAISS.load_local(
                    "faiss_index",
                    embedding_model,
                    allow_dangerous_deserialization=True
                )

                # =================================================
                # RETRIEVER
                # =================================================

                retriever = vector_store.as_retriever(
                    search_kwargs={
                        "k": 4
                    }
                )

                # =================================================
                # RETRIEVE DOCUMENTS
                # =================================================

                docs = retriever.invoke(
                    question
                )

                # =================================================
                # BUILD CONTEXT
                # =================================================

                context_parts = []

                for doc in docs:

                    context_parts.append(
                        doc.page_content
                    )

                context = "\n\n".join(
                    context_parts
                )


            # =================================================
            # GEMINI
            # =================================================

            with st.spinner(
                "🤖 Generating answer..."
            ):

                llm = ChatGoogleGenerativeAI(
                    model="gemini-3.5-flash",
                    google_api_key=GOOGLE_API_KEY,
                    temperature=0
                )

                # =================================================
                # PROMPT
                # =================================================

                prompt = f"""
You are an AI Financial Report Assistant.

Your job is to answer questions about the uploaded
financial report.

IMPORTANT RULES:

1. Answer ONLY using the provided context.
2. Do not use outside knowledge.
3. Do not invent numbers or facts.
4. If the answer is not available in the context,
   clearly say that the information could not be found
   in the uploaded report.
5. Give a concise and professional answer.
6. When financial figures are available, mention
   the appropriate units such as million or billion.

--------------------------------------------------
REPORT CONTEXT
--------------------------------------------------

{context}

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
ANSWER
--------------------------------------------------
"""

                response = llm.invoke(
                    prompt
                )


            # =================================================
            # SAVE QUESTION
            # =================================================

            if question not in st.session_state.questions:

                st.session_state.questions.insert(
                    0,
                    question
                )

            st.session_state.questions = (
                st.session_state.questions[:5]
            )


            # =================================================
            # DISPLAY ANSWER
            # =================================================

            st.subheader(
                "💡 Answer"
            )

            with st.container(border=True):

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


            # =================================================
            # DISPLAY SOURCES
            # =================================================

            st.subheader(
                "📚 Sources"
            )

            for i, doc in enumerate(
                docs,
                start=1
            ):

                page = doc.metadata.get(
                    "page",
                    None
                )

                if isinstance(page, int):

                    page_number = page + 1

                elif page is not None:

                    page_number = page

                else:

                    page_number = "Unknown"

                with st.container(border=True):

                    st.write(
                        f"📄 **Source {i}**"
                    )

                    st.caption(
                        f"Page {page_number}"
                    )


        except Exception as e:

            st.error(
                "❌ Something went wrong."
            )

            st.exception(e)


# ============================================================
# RECENT QUESTIONS
# ============================================================

if st.session_state.questions:

    st.divider()

    st.subheader(
        "🕘 Recent Questions"
    )

    for i, previous_question in enumerate(
        st.session_state.questions,
        start=1
    ):

        with st.container(border=True):

            st.write(
                f"**{i}.** {previous_question}"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "💰 AI Financial Assistant • "
    "RAG-based Financial Report Analysis"
)
