# Student Names: Amina O. & Ossama Z.
# RAG Assignment - Space Exploration Assistant
import streamlit as st
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- Configuration ---
PERSIST_DIRECTORY = "./chroma_db"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama3"  # Ensure you have pulled this model using `ollama pull llama3`

# --- UI Setup ---
st.set_page_config(page_title="Space Explorer RAG", page_icon="🚀", layout="wide")

st.title("🚀 Space Exploration AI Assistant")
st.markdown("""
This is a **Local RAG Application** for the Information Retrieval Final Assignment.
It uses **Wikipedia data** (SpaceX, NASA, etc.), **ChromaDB** for storage, and **Ollama** for the LLM.
""")

# --- Sidebar ---
st.sidebar.header("Configuration")
model_name = st.sidebar.selectbox("Select Local LLM", ["llama3", "mistral", "gemma"], index=0)
st.sidebar.info(f"Ensure that `{model_name}` is installed via Ollama.")

# --- Load Vector Store ---
@st.cache_resource
def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    if not os.path.exists(PERSIST_DIRECTORY):
        return None
    vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    return vectorstore

vectorstore = load_vectorstore()

if not vectorstore:
    st.error("Vector Database not found! Please run the `data_ingestion.ipynb` notebook first to build the index.")
    
# --- RAG Setup ---
if vectorstore:
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # Define the Prompt
    template = """Answer the question based ONLY on the following context:
    {context}

    Question: {question}
    
    If you don't know the answer based on the context, say "I don't have enough information in my database."
    Keep the answer concise and informative.
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Initialize LLM
    try:
        llm = ChatOllama(model=model_name)
    except Exception as e:
        st.error(f"Error connecting to Ollama: {e}. Make sure Ollama is running.")
        llm = None

    if llm:
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # --- Chat Interface ---
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if query := st.chat_input("Ask a question about space exploration..."):
            st.session_state.messages.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)

            with st.chat_message("assistant"):
                with st.spinner("Searching the cosmos..."):
                    try:
                        response = chain.invoke(query)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"Error generating response: {e}")
