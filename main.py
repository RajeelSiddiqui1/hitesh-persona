import streamlit as st
import json
import os
from openai import OpenAI

st.set_page_config(
    page_title="Hitesh Choudhary AI",
    page_icon="https://hiteshchoudhary.com/favicon.png",
    layout="centered",
    initial_sidebar_state="expanded"
)

client = OpenAI(
    api_key="AIzaSyANS_IgqAk3B4RTGv3SCGLtgwbjYtV9-UU",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You are Hitesh Choudhary from the Chai aur Code YouTube channel. You also have an English channel.

Respond only in Roman Urdu, maintaining Hitesh's lively and motivational style, as if in a live stream, with humor and encouragement.

Social Media:
| Platform           | Handle / URL                                                                                  |
| ------------------ | --------------------------------------------------------------------------------------------- |
| **YouTube** (main) | [youtube.com/@HiteshCodeLab](https://www.youtube.com/channel/UCXgGY0wkgOzynnHvSEVmE3A/about)   |
| **YouTube** (vlog) | [youtube.com/@hiteshChoudhary](https://www.youtube.com/@hiteshChoudhary)                       |
| **Twitter / X**    | [@Hiteshdotcom](https://twitter.com/Hiteshdotcom)                                             |
| **Instagram**      | [@hiteshchoudharyofficial](https://www.instagram.com/hiteshchoudharyofficial)                   |
| **LinkedIn**       | [linkedin.com/in/hiteshchoudhary](https://in.linkedin.com/in/hiteshchoudhary)                   |
| **Discord**        | [hitesh.ai/discord](https://hitesh.ai/discord)                                                |
| **Personal site**  | [hiteshchoudhary.com](https://hiteshchoudhary.com)                                             |
"""

MESSAGE_FILE = "hitesh_chat_history.json"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
html, body, [class*="st-"] {
    font-family: 'Roboto', sans-serif;
    background: linear-gradient(180deg, #0D1B2A 0%, #1E2A44 100%);
}
.stApp {
    background: transparent;
    box-shadow: 0 0 20px rgba(21, 101, 192, 0.3);
}
[data-testid="stSidebar"] {
    background: linear-gradient(145deg, #0D1B2A, #1E2A44);
    border: 2px solid #FFFFFF;
    box-shadow: 0 0 15px rgba(21, 101, 192, 0.7);
}
[data-testid="stSidebar"] .st-emotion-cache-17lntkn {
    color: #B3C7F7;
}
[data-testid="stSidebarNav"] {
    position: relative;
    padding: 10px;
}
[data-testid="stSidebarNav"]::before {
    content: '▶';
    color: #FF6200;
    font-size: 1.5rem;
    position: absolute;
    top: 10px;
    right: 10px;
    transition: all 0.3s ease;
}
[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarNav"]::before {
    content: '◀';
    color: #FFFFFF;
}
[data-testid="stSidebarNav"]:hover::before {
    color: #1565C0;
    text-shadow: 0 0 10px rgba(21, 101, 192, 0.7);
}
.profile-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem 0;
    text-align: center;
}
.profile-img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 4px solid #FF6200;
    margin-bottom: 1rem;
    box-shadow: 0 0 20px rgba(21, 101, 192, 0.7);
}
.profile-name {
    font-size: 1.8rem;
    font-weight: 700;
    color: #B3C7F7;
}
.profile-tagline {
    font-size: 1rem;
    color: #6B7280;
}
.social-links {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1rem;
}
.social-links a {
    color: #6B7280;
    font-size: 1.5rem;
    transition: color 0.3s, transform 0.3s;
}
.social-links a:hover {
    color: #1565C0;
    transform: scale(1.2);
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(145deg, #FF6200, #E65100);
    color: #FFFFFF;
    border: 2px solid #FFFFFF;
    font-weight: 700;
    padding: 0.75rem 1.5rem;
    box-shadow: 0 4px 12px rgba(21, 101, 192, 0.5);
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: #1565C0;
    border: 2px solid #FF6200;
    box-shadow: 0 0 20px rgba(21, 101, 192, 0.8);
}
.stButton>button:focus {
    box-shadow: 0 0 15px rgba(255, 98, 0, 0.7);
}
[data-testid="stChatInput"] {
    background: #0D1B2A;
}
[data-testid="stChatInput"] textarea {
    background: #0D1B2A;
    border: 2px solid #FFFFFF;
    border-radius: 10px;
    color: #B3C7F7;
    box-shadow: 0 0 10px rgba(21, 101, 192, 0.5);
}
[data-testid="stChatInput"] textarea:focus {
    border: 2px solid #FF6200;
    box-shadow: 0 0 15px rgba(21, 101, 192, 0.8);
}
[data-testid="stChatMessage"] {
    gap: 1rem;
}
.st-emotion-cache-4oy321 {
    background: #1E2A44;
    border: 2px solid #FFFFFF;
    box-shadow: 0 4px 15px rgba(21, 101, 192, 0.6);
    border-radius: 15px;
    padding: 1.5rem;
}
.st-emotion-cache-4oy321 p {
    margin: 0;
    color: #B3C7F7;
    line-height: 1.8;
}
[data-testid="stChatMessage"] .st-emotion-cache-1c7y2kd {
    font-weight: 700;
    color: #FF6200;
}
::-webkit-scrollbar {
    width: 10px;
}
::-webkit-scrollbar-track {
    background: #0D1B2A;
}
::-webkit-scrollbar-thumb {
    background: #1E2A44;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #1565C0;
}
.welcome-container {
    text-align: center;
    padding: 4rem 1rem;
    color: #B3C7F7;
}
.welcome-icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    color: #1565C0;
}
.welcome-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #FF6200;
}
.welcome-text {
    color: #6B7280;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}
.example-prompts {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    flex-wrap: wrap;
}
.example-prompt {
    background: #1E2A44;
    border: 1px solid #1E2A44;
    padding: 0.75rem 1.5rem;
    border-radius: 25px;
    cursor: pointer;
    color: #B3C7F7;
    transition: all 0.3s;
}
.example-prompt:hover {
    border-color: #FF6200;
    color: #1565C0;
    box-shadow: 0 0 10px rgba(21, 101, 192, 0.7);
}
</style>
""", unsafe_allow_html=True)

def load_chat_history():
    if os.path.exists(MESSAGE_FILE):
        try:
            with open(MESSAGE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return [{"role": "system", "content": SYSTEM_PROMPT}]
    return [{"role": "system", "content": SYSTEM_PROMPT}]

def save_chat_history(messages):
    with open(MESSAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=4)

def clear_chat_history():
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    save_chat_history(st.session_state.messages)
    st.toast("🧹 Chat history saaf ho gayi! Nayi shuruaat!", icon="🎉")

with st.sidebar:
    st.markdown("""
    <div class="profile-container">
        <img src="https://media.licdn.com/dms/image/v2/D4D03AQH8CXRHAKQd6Q/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1693777638244?e=2147483647&v=beta&t=cxdOsxsjBWd3eicb9qXbHav_8RN4horjNSi4g18M16g" class="profile-img">
        <div class="profile-name">Hitesh Choudhary AI</div>
        <div class="profile-tagline">Chai Piyo, Code Karo!</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <h3 style='text-align: center; color: #B3C7F7;'>Socials pe milte hain!</h3>
    <div class="social-links">
        <a href="https://youtube.com/chaiaurcode" target="_blank" title="YouTube">📺</a>
        <a href="https://twitter.com/hiteshdotcom" target="_blank" title="Twitter/X">🐦</a>
        <a href="https://instagram.com/hiteshchoudharyofficial" target="_blank" title="Instagram">📸</a>
        <a href="https://linkedin.com/in/hiteshchoudhary" target="_blank" title="LinkedIn">💼</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🧹 Chat History Saaf Karo"):
        clear_chat_history()

if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    avatar = "👤" if message["role"] == "user" else "https://avatars.githubusercontent.com/u/11613311?v=4"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if len(st.session_state.messages) <= 1:
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-icon">☕</div>
        <div class="welcome-title">Chai aur Code AI mein swagat hai!</div>
        <p class="welcome-text">Main Hitesh Choudhary ka AI version hoon.<br>Code, career, ya tech ke baare mein kuch bhi pooch sakte ho!</p>
    </div>
    """, unsafe_allow_html=True)

if prompt := st.chat_input("Apna sawaal yahan likho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="https://avatars.githubusercontent.com/u/11613311?v=4"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Soch raha hoon, chai ke saath... 🤔")
        
        api_messages = []
        for msg in st.session_state.messages:
            if msg["role"] == "assistant":
                try:
                    parsed_content = json.loads(msg["content"])
                    api_messages.append({"role": "assistant", "content": parsed_content.get("response", "")})
                except (json.JSONDecodeError, TypeError):
                    api_messages.append({"role": "assistant", "content": msg["content"]})
            else:
                api_messages.append(msg)
        
        try:
            with st.spinner("Chai ban rahi hai... jawab aa raha hai..."):
                response = client.chat.completions.create(
                    model="gemini-2.5-flash",
                    response_format={"type": "json_object"},
                    messages=api_messages
                )
            
            raw_content = response.choices[0].message.content
            parsed_content = json.loads(raw_content)
            assistant_reply = parsed_content.get("response", "Kuch garbar ho gayi, dost.")
            
            message_placeholder.markdown(assistant_reply)
            
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            save_chat_history(st.session_state.messages)
        
        except Exception as e:
            error_message = f"Arre! Connection mein kuch issue hai: {str(e)}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})