import streamlit as st

# 1. Set up the title of your web page
st.title("My Online Chatbot")

# 2. Create a place for the user to type
user_input = st.chat_input("Type your message here...")

# 3. If the user types something, show it on the screen
if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    # This is where the bot "thinks"
    with st.chat_message("assistant"):
        st.write(f"You said: {user_input}. I'm working on getting my AI brain connected!")
