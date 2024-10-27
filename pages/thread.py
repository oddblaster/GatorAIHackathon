import streamlit as st

# Initialize the session state for messages if not already done
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Title
st.title("Anonymous Help Board")

# Display all messages
st.subheader("Messages from Others Who Need Help:")
for idx, message in enumerate(reversed(st.session_state['messages'])):
    st.write(f"Message {len(st.session_state['messages']) - idx}: {message}")
