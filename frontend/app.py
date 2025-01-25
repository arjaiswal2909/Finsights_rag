import streamlit as st
import fitz
import requests
import io

st.set_page_config(layout="wide", page_title="Finance RAG on Semi-Structured PDF", page_icon="📄")

BACKEND_URL = "http://127.0.0.1:4892"  
def display_pdf_sidebar(pdf_file, zoom):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page_number, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            img = pix.tobytes("png")
            st.image(img, use_container_width=True, caption=f"Page {page_number}")
    except Exception as e:
        st.error(f"Error processing PDF: {e}")

# Sidebar for PDF upload and zoom level
with st.sidebar:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    zoom_level = st.slider("Zoom Level", min_value=1.0, max_value=3.0, step=0.1, value=1.0)

    if uploaded_file is not None:
        st.subheader("PDF Preview")
        with st.spinner("Rendering PDF..."):
            display_pdf_sidebar(uploaded_file, zoom_level)
        
        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                pdf_bytes = uploaded_file.getvalue()
                response = requests.post(f"{BACKEND_URL}/process_pdf", files={"file": pdf_bytes})
                if response.status_code == 200:
                    st.success("PDF processed successfully!")
                    st.session_state["processed"] = True
                else:
                    st.error("Failed to process PDF. Please try again.")
    else:
        st.info("Please upload a PDF file to view.")

# Initialize chat session
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.title("Finance RAG on Semi-Structured PDF")

# Chat display section
st.markdown(
    """
    <style>
    .chat-container {
        height: 400px;
        overflow-y: auto;
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fafafa;
        display: flex;
        flex-direction: column;
    }
    .user-message, .assistant-message {
        padding: 10px;
        margin: 5px 0;
        border-radius: 15px;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-message {
        align-self: flex-end;
        background-color: #e0f7fa;
        color: #005662;
    }
    .assistant-message {
        align-self: flex-start;
        background-color: #ffffff;
        color: #333;
        border: 1px solid #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for chat in st.session_state["chat_history"]:
    if chat["role"] == "user":
        st.markdown(f"<div class='user-message'>{chat['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-message'>{chat['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Query input and send button
col1, col2 = st.columns([4, 1])
with col1:
    query_input = st.text_input("Your Message", placeholder="Enter your query here...", key="user_input", label_visibility="collapsed")
with col2:
    if st.button("Send", use_container_width=True):
        if query_input.strip():
            response = requests.post(f"{BACKEND_URL}/query", json={"query": query_input})
            if response.status_code == 200:
                answer = response.json().get("answer", "No response received.")
                st.session_state["chat_history"].append({"role": "user", "content": query_input})
                st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                st.rerun()
            else:
                st.error("Failed to get response. Please try again.")
        else:
            st.warning("Please enter a valid query.")
