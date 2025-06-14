import streamlit as st
from openai import OpenAI
from quiz import get_random_question
from dotenv import load_dotenv
import os
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer
import av

# Load .env dan API Key Together
load_dotenv()
api_key = ("2fd0b25bb9a726303e7834d43a1633c01b381cc23ddfc76df2fba8af102d333d")

# Inisialisasi OpenAI client via Together.ai
client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")

# Konfigurasi halaman
st.set_page_config(page_title="🎓 Edubot - Kuis & Chat Edukasi", layout="centered")

# CSS untuk mempercantik tampilan
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #83a4d4, #b6fbff);
        color: #ffffff;
    }
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1603983811474-59e8c5e0d04e");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    h1, h2, h3, h4 {
        color: #ffffff;
        text-shadow: 1px 1px 2px #000000;
    }
    .stButton>button {
        background-color: #008CBA;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #005f73;
    }
    .stTextInput>div>div>input {
        background-color: #f0f8ff;
        border-radius: 5px;
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='main'>", unsafe_allow_html=True)
st.title("🤖 Edubot - Kuis & Chat Edukasi Interaktif")

# --- Bagian Chat Edukasi ---
st.header("💬 Tanya Edubot")
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Kamu adalah asisten edukatif ramah yang menjawab pertanyaan secara sederhana dan mendidik."}
    ]

# --- Input suara ---
st.markdown("### 🎙️ Gunakan Suara untuk Bertanya")
if st.button("🔊 Mulai Rekam & Transkrip"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Silakan bicara...")
        try:
            audio = recognizer.listen(source, timeout=5)
            voice_text = recognizer.recognize_google(audio, language='id-ID')
            st.success(f"🗣️ Terdeteksi: {voice_text}")
            st.session_state.voice_input = voice_text
        except Exception as e:
            st.error(f"Gagal mengenali suara: {e}")
else:
    st.session_state.voice_input = ""

user_question = st.text_input("Tanyakan sesuatu kepada Edubot:", value=st.session_state.voice_input if "voice_input" in st.session_state else "")
if st.button("📩 Kirim Pertanyaan"):
    if user_question:
        st.session_state.messages.append({"role": "user", "content": user_question})
        try:
            with st.spinner("Edubot sedang menjawab..."):
                response = client.chat.completions.create(
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    messages=st.session_state.messages,
                    temperature=0.7
                )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.success("✅ Edubot menjawab:")
            st.markdown(reply)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# Tampilkan histori chat
if len(st.session_state.messages) > 1:
    st.markdown("---")
    st.subheader("📝 Riwayat Chat:")
    for m in st.session_state.messages[1:]:
        role = "👤 Kamu" if m["role"] == "user" else "🤖 Edubot"
        st.markdown(f"**{role}:** {m['content']}")

# --- Bagian Kuis Interaktif ---
st.markdown("---")
st.header("🧠 Kuis Pertanyaan Acak")

if "question" not in st.session_state:
    st.session_state.question = None
if "score" not in st.session_state:
    st.session_state.score = 0

if st.button("🎲 Mulai Pertanyaan Acak"):
    st.session_state.question = get_random_question()
    st.session_state.user_answer = ""

if st.session_state.question:
    st.subheader("❓ Pertanyaan:")
    st.markdown(f"<div style='font-size:18px; margin-bottom:10px'>{st.session_state.question['question']}</div>", unsafe_allow_html=True)

    answer = st.text_input("Jawaban Anda:", key="user_answer_input")

    if st.button("✅ Kirim Jawaban"):
        correct = st.session_state.question["answer"].strip().lower()
        user = answer.strip().lower()
        if user == correct:
            st.success("🎉 Jawaban benar!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Salah. Jawaban yang benar: **{st.session_state.question['answer']}**")

        st.markdown(f"<h4>🎯 Skor Saat Ini: <span style='color:green'>{st.session_state.score}</span></h4>", unsafe_allow_html=True)
        st.session_state.question = None

st.markdown("</div>", unsafe_allow_html=True)
