import streamlit as st
from openai import OpenAI

# This line grabs the key from the "Secret vault" you just filled
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI RAG Chatbot", layout="wide")
st.title("📄 AI Document Assistant")

# --- 1. SETTINGS & SIDEBAR ---
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    uploaded_file = st.file_uploader("Upload a document (.txt only for now)", type=("txt"))
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 2. INITIALIZE CHAT HISTORY (Requirement 1) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history on every rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. THE RAG PIPELINE (Requirement 4 & 5) ---
context = ""
if uploaded_file is not None:
    # Efficiency: We read the file once and store it as context (Requirement 2)
    context = uploaded_file.read().decode("utf-8")
    st.sidebar.success("Document attached to context!")

# --- 4. CHAT LOGIC (Requirement 3) ---
if prompt := st.chat_input("Ask a question about your file..."):
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar.")
    else:
        client = OpenAI(api_key=api_key)
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Build the AI's "Brain" with the RAG Context
        system_message = "You are a helpful assistant."
        if context:
            system_message += f"\n\nUse the following document text to answer: {context}"

        # Combine history + current prompt for the API call
        messages_for_api = [{"role": "system", "content": system_message}] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]

        # Call OpenAI
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages_for_api
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
