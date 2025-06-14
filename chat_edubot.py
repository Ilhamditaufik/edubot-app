# chat_edubot.py
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API Key dari .env
load_dotenv()
api_key =("2fd0b25bb9a726303e7834d43a1633c01b381cc23ddfc76df2fba8af102d333d")  # Ganti jika variabel .env kamu berbeda

# Konfigurasi OpenAI API (via Together.ai endpoint)
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")

# Setup halaman
st.set_page_config(page_title="Edubot - Chat Edukasi", layout="wide")
st.title("🤖 Edubot - Chat Edukasi")

# Inisialisasi riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Kamu adalah Edubot, asisten edukasi ramah dan pintar yang membantu menjelaskan pelajaran untuk anak SMA."}
    ]

# Layout 2 kolom
col1, col2 = st.columns([1, 2])

# Kolom kiri: Riwayat Chat
with col1:
    st.subheader("📜 Riwayat Obrolan")
    for msg in st.session_state.messages[1:]:  # skip system prompt
        role = "🧑‍🎓 Kamu" if msg["role"] == "user" else "🤖 Edubot"
        with st.chat_message(role):
            st.markdown(msg["content"])

# Kolom kanan: Chat Input
with col2:
    prompt = st.text_input("💬 Tanyakan sesuatu tentang pelajaran:")

    if st.button("Kirim"):
        if prompt:
            # Tambahkan pertanyaan user
            st.session_state.messages.append({"role": "user", "content": prompt})

            try:
                # Dapatkan respons dari Together AI (GPT via openai client)
                response = client.chat.completions.create(
                    model="meta-llama/Llama-3-8b-chat-hf",
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                bot_reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                st.success("✅ Edubot sudah menjawab!")

            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
