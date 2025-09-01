import streamlit as st
from cohost.generator import generate_with_history
from cohost.persona import PERSONA_PREFIX
from cohost.tts import tts_save_wav_pyttsx3

st.set_page_config(page_title="Generative Podcast Co-Host", layout="wide")
st.title("Generative Podcast Co-Host (Local)")

# Initialize session state
if "chat_history_ids" not in st.session_state:
    st.session_state.chat_history_ids = None
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of (role, text)

# Input
user_input = st.text_input("You:", key="input")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Send"):
        if user_input and user_input.strip():
            # Prepend persona prefix and role context
            prompt = f"{PERSONA_PREFIX}\n[User]: {user_input}\n[Co-Host]:"
            
            new_history, reply = generate_with_history(
                st.session_state.chat_history_ids,
                prompt
            )
            st.session_state.chat_history_ids = new_history
            st.session_state.messages.append(("You", user_input))
            st.session_state.messages.append(("Co-Host", reply))
            st.rerun()
        else:
            st.warning("Enter something.")

with col2:
    if st.button("Reset Conversation"):
        st.session_state.chat_history_ids = None
        st.session_state.messages = []
        st.success("Conversation reset")

# Display messages
for role, text in st.session_state.messages[-20:]:
    if role == "You":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Co-Host:** {text}")

# Play audio for last co-host message
if st.session_state.messages:
    last_role, last_text = st.session_state.messages[-1]
    if last_role == "Co-Host":
        wav = tts_save_wav_pyttsx3(last_text)
        if wav:
            st.audio(wav, format="audio/wav")
