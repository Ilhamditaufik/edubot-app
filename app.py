import streamlit as st
import openai
from quiz_data import get_question
import speech_recognition as sr
from gtts import gTTS
import os
import json
import smtplib
from email.message import EmailMessage


# 🟢 API KEY
openai.api_key = "tgp_v1_pRd7ya0V8UWwKlgyWmSU5Cm3JktDlEqNc2_JtZSArOU"
openai.api_base = "https://api.together.xyz/v1"

EMAIL_SENDER = "ilham030918@gmail.com"
EMAIL_PASSWORD = "ilhamdi26"

# ✅ Inisialisasi awal session state agar tidak error
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True  # Bypass login
if "username" not in st.session_state:
    st.session_state.username = "Guest"
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Kamu adalah asisten edukatif ramah yang menjawab pertanyaan secara sederhana dan mendidik."}
    ]



# ============================
# 💾 Dummy User Data
# ============================
users = {
    "admin": "password123",
    "user1": "abc123",
    "user2": "def456",
    "ilhamdi": "ilham123"
}

# ============================
# 💾 Histori File Helper
# ============================
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# Sidebar Riwayat Chat
with st.sidebar:
    st.markdown("### 🗂️ Ringkasan Riwayat Chat")
    if "messages" in st.session_state and len(st.session_state.messages) > 1:
        for i, m in enumerate(st.session_state.messages[1:]):
            role = "🧑 Kamu" if m["role"] == "user" else "🤖 Edubot"
            content = m["content"]
            st.markdown(f"**{role} {i+1}:** {content[:40]}{'...' if len(content)>40 else ''}")
    else:
        st.info("Belum ada riwayat chat.")

# Sidebar Download Riwayat
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Download Riwayat Chat")
if "messages" in st.session_state and len(st.session_state.messages) > 1:
    chat_text = ""
    for m in st.session_state.messages[1:]:
        role = "Kamu" if m["role"] == "user" else "Edubot"
        chat_text += f"{role}:\n{m['content']}\n\n"

    st.sidebar.download_button(
        label="💾 Unduh sebagai TXT",
        data=chat_text,
        file_name="riwayat_chat_edubot.txt",
        mime="text/plain"
    )
else:
    st.sidebar.info("Belum ada chat untuk diunduh.")


# ===============================
# 📧 Kirim Email Riwayat Chat
# ===============================
st.sidebar.markdown("---")
st.sidebar.markdown("### 📧 Kirim Riwayat Chat ke Email")

if "messages" in st.session_state and len(st.session_state.messages) > 1:
    recipient_email = st.sidebar.text_input("Masukkan alamat email:")
    
    if st.sidebar.button("✉️ Kirim Email"):
        if recipient_email:
            # Gabungkan chat
            chat_text = ""
            for m in st.session_state.messages[1:]:
                role = "Kamu" if m["role"] == "user" else "Edubot"
                chat_text += f"{role}:\n{m['content']}\n\n"
                
            # Buat email
            msg = EmailMessage()
            msg["Subject"] = "Riwayat Chat Edubot Kamu"
            msg["From"] = EMAIL_SENDER
            msg["To"] = recipient_email
            msg.set_content("Halo,\n\nBerikut lampiran riwayat chat kamu dengan Edubot.\n\nSalam,\nEdubot")
            msg.add_attachment(chat_text.encode("utf-8"), maintype="text", subtype="plain", filename="riwayat_chat_edubot.txt")
            
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                    smtp.send_message(msg)
                st.sidebar.success("✅ Email berhasil dikirim!")
            except Exception as e:
                st.sidebar.error(f"Gagal mengirim email: {e}")
        else:
            st.sidebar.warning("Masukkan alamat email terlebih dahulu.")
else:
    st.sidebar.info("Belum ada chat untuk dikirim.")


# ============================
# 🎨 Background & Tema
# ============================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #e1bee7);
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

bg_light = "#d7e9f7"
bg_dark = "#1f2c3a"
text_light = "#222222"
text_dark = "#eeeeee"

theme_color = bg_light if st.session_state.theme_mode == "light" else bg_dark
text_color = text_light if st.session_state.theme_mode == "light" else text_dark

st.markdown(
    f"""
    <style>
    .stApp {{
        background: #263238;  /* abu kebiruan gelap */
        background-attachment: fixed;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {text_color};
    }}
    .stTextInput > div > div > input {{
        background-color: #1c2d4a;
        color: #ffffff;
        border: 1px solid #3a506b;
        border-radius: 6px;
        padding: 8px;
    }}
    .stButton > button {{
        background-color: #3a506b;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
    }}
    .stButton > button:hover {{
        background-color: #5bc0be;
        color: #0b1a33;
    }}
    .stSelectbox > div > div {{
        background-color: #1c2d4a;
        color: #ffffff;
        border: 1px solid #3a506b;
        border-radius: 6px;
    }}
    .stDownloadButton > button {{
        background-color: #3a506b;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
    }}
    .stDownloadButton > button:hover {{
        background-color: #5bc0be;
        color: #0b1a33;
    }}
    .stAudio, .stVideo {{
        border-radius: 8px;
        overflow: hidden;
        margin-top: 10px;
        margin-bottom: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #1c2d4a;
        color: #ffffff;
        border-radius: 6px 6px 0 0;
        padding: 6px 12px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #3a506b;
        color: #ffffff;
    }}

    /* ✨ Video Card Styling + Animasi */
    .video-card {{
        background-color: #1c2d4a;
        border: 1px solid #3a506b;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        animation: fadeInUp 0.6s ease forwards;
        opacity: 0;
        transform: translateY(20px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .video-card:hover {{
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(91,192,190,0.5);
    }}
    .video-title {{
        color: #ffffff;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
    }}
    .stVideo {{
        border-radius: 8px;
        overflow: hidden;
    }}

    /* 🔥 Keyframe Animasi */
    @keyframes fadeInUp {{
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)



# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat Edukasi", "🧠 Kuis", "🎥 Tonton Edukasi"])

# ============================
# 💬 Chat Edukasi
# ============================
with tab1:
    st.title("🤖 Edubot - Chat Edukasi Interaktif")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Kamu adalah asisten edukatif ramah yang menjawab pertanyaan secara sederhana dan mendidik."}
        ]

    

    user_question = st.text_input(
    "Tanyakan sesuatu kepada Edubot:",
    value=""
    )



    import requests

if st.button("📩 Kirim Pertanyaan"):
    if user_question.strip() != "":
        st.session_state.messages.append({"role": "user", "content": user_question})

        with st.spinner("Edubot sedang menjawab..."):
            headers = {
                "Authorization": f"Bearer {openai.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "messages": st.session_state.messages,
                "temperature": 0.7
            }
            response = requests.post(
                "https://api.together.xyz/v1/chat/completions",
                headers=headers,
                json=data
            )
            if response.status_code == 200:
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
                st.session_state.messages.append({"role": "assistant", "content": reply})

                st.markdown(
                    """
                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" alt="Bot Avatar"
                        style="width:40px;height:40px;margin-right:10px;">
                        <span style="font-weight:bold;font-size:18px;">Edubot menjawab:</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.success("✅ Edubot menjawab:")
                st.markdown(reply)
            else:
                st.error(f"Terjadi kesalahan API: {response.text}")
    else:
        st.warning("Pertanyaan tidak boleh kosong.")

# ===============================
# 🧠 KUIS DENGAN LEVEL, TIMER, SKOR, LEADERBOARD
# ===============================
with tab2:
    import time
    import datetime
    from quiz_data import get_question

    st.header("🧠 Kuis Edukasi Interaktif")
    st.markdown("<br>", unsafe_allow_html=True)

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "leaderboard" not in st.session_state:
        st.session_state.leaderboard = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # Pilih tingkat kesulitan
    level = st.selectbox("📊 Pilih Tingkat Kesulitan", ["Mudah", "Sedang", "Sulit"])

    # Mulai Kuis
    if st.button("🎲 Mulai Pertanyaan"):
        st.session_state.current_question = get_question(level)
        st.session_state.start_time = time.time()
        st.session_state.user_answer = ""
        st.session_state.timer_active = True

    if st.session_state.current_question is not None:
        q = st.session_state.current_question.get("question", "")
        answer = st.session_state.current_question.get("answer", "").strip().lower()

        st.subheader(f"❓ {q}")
        remaining = 30 - int(time.time() - st.session_state.start_time)

        # Timer
        if remaining > 0:
            st.info(f"⏳ Waktu tersisa: {remaining} detik")
        else:
            st.warning("⏰ Waktu habis!")
            st.session_state.current_question = None
            st.stop()

        # Input jawaban
        user_input = st.text_input("💬 Jawaban Anda:")

        # Dua tombol dalam satu baris
        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Kirim Jawaban"):
                if remaining <= 0:
                    st.error("Jawaban tidak diterima. Waktu habis!")
                else:
                    if user_input.strip().lower() == answer:
                        st.success("✅ Jawaban BENAR!")
                        st.session_state.score += 1
                    else:
                        st.error(f"❌ Salah! Jawaban: **{answer}**")

                    # Simpan leaderboard
                    st.session_state.leaderboard.append({
                        "nama": st.session_state.username,
                        "skor": st.session_state.score,
                        "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

                    st.session_state.current_question = None

        with col2:
            if st.button("➡️ Soal Selanjutnya"):
                st.session_state.current_question = get_question(level)
                st.session_state.start_time = time.time()
                st.session_state.user_answer = ""
                st.stop()


    st.markdown("---")

    # Skor
    st.markdown(f"🎯 **Skor Saat Ini:** {st.session_state.score}")

    # Leaderboard
    if st.button("🏆 Lihat Leaderboard"):
        st.subheader("🏅 Leaderboard")
        sorted_lb = sorted(st.session_state.leaderboard, key=lambda x: x["skor"], reverse=True)
        for i, entry in enumerate(sorted_lb):
            st.markdown(f"{i+1}. **{entry['nama']}** - {entry['skor']} poin - {entry['waktu']}")

    # Sertifikat PDF
    if st.session_state.score >= 3:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 24)
        pdf.cell(0, 20, "Sertifikat Kuis Edukasi", ln=True, align="C")
        pdf.set_font("Arial", "", 16)
        pdf.multi_cell(0,10,f"Ini menyatakan bahwa {st.session_state.username} telah mencapai skor {st.session_state.score} dalam Kuis Edukasi Edubot.",align="C")
        pdf.output("sertifikat.pdf")

        with open("sertifikat.pdf", "rb") as f:
            st.download_button("🎓 Unduh Sertifikat PDF", f, file_name="sertifikat_kuis.pdf")


# ===============================
# 🎥 TONTON EDUKASI
# ===============================
with tab3:
    st.header("🎥 Video Edukasi")
    st.markdown("<br>", unsafe_allow_html=True)

    def video_block(title, url):
        with st.container():
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="video title">{title}</div>', unsafe_allow_html=True)
            st.video(url)
            st.markdown("<br>", unsafe_allow_html=True)

    video_list = [
        ("1️⃣ Dasar Pemrograman", "https://www.youtube.com/watch?v=jGyYuQf-GeE&list=PLFIM0718LjIWonBxVAM2NgNuW0YxQverx"),
        ("2️⃣ Geografi & Bumi", "https://www.youtube.com/watch?v=eR5OXHNJyLc"),
        ("3️⃣ Kimia Dasar", "https://www.youtube.com/watch?v=FSyAehMdpyI"),
        ("4️⃣ Fisika Dasar", "https://www.youtube.com/watch?v=4HrweW4IqJc"),
        ("5️⃣ Biologi Sel", "https://www.youtube.com/watch?v=URUJD5NEXC8"),
        ("6️⃣ Matematika Dasar", "https://www.youtube.com/watch?v=V6yixyiJcos"),
        ("7️⃣ Sejarah Indonesia", "https://www.youtube.com/watch?v=nM4mitSBQKk"),
        ("8️⃣ Bahasa Inggris Dasar", "https://www.youtube.com/watch?v=YkLjqFpBh84"),
        ("9️⃣ Astronomi", "https://www.youtube.com/watch?v=0rHUDWjR5gg"),
        ("🔟 Ekonomi Dasar", "https://www.youtube.com/watch?v=PnrCODo7pd8"),
        ("1️⃣1️⃣ Ekosistem", "https://www.youtube.com/watch?v=o3wOlOjYdWg"),
        ("1️⃣2️⃣ Energi Terbarukan", "https://www.youtube.com/watch?v=JzZGD7UXRyM"),
        ("1️⃣3️⃣ Sistem Tata Surya", "https://www.youtube.com/watch?v=libKVRa01L8"),
        ("1️⃣4️⃣ Pendidikan Karakter", "https://www.youtube.com/watch?v=qq5ggBr0bTM"),
        ("1️⃣5️⃣ Perubahan Iklim", "https://www.youtube.com/watch?v=ifrHogDujXw"),
        ("1️⃣6️⃣ Pertanian Modern", "https://www.youtube.com/watch?v=0RbtFhkONFU"),
        ("1️⃣7️⃣ Teknologi Informasi", "https://www.youtube.com/watch?v=HJiKsYy9efI"),
        ("1️⃣8️⃣ Robotika Dasar", "https://www.youtube.com/watch?v=JMUxmLyrhSk"),
        ("1️⃣9️⃣ Pemrograman Python Pemula", "https://www.youtube.com/watch?v=_uQrJ0TkZlc"),
        ("2️⃣0️⃣ Kewirausahaan", "https://www.youtube.com/watch?v=bRcu-ysocX4"),
        ("2️⃣1️⃣ Mengenal Sistem Tata Surya dan Planet-Planet", "https://www.youtube.com/watch?v=jFIz8izir3U"),
        ("2️⃣2️⃣ Evolusi Kehidupan di Bumi: Dari Mikroba ke Manusia", "https://www.youtube.com/watch?v=q-RmDmtV1tE"),
        ("2️⃣3️⃣ Penemu Hebat Dunia", "https://www.youtube.com/watch?v=hxQ0khaqktc"),
        ("2️⃣4️⃣ Mekanika Fluida", "https://www.youtube.com/watch?v=W3LcNXWuOdM"),
        ("2️⃣5️⃣ Pemrograman Web", "https://www.youtube.com/watch?v=t8Nxs7F4qEM&list=PLjRBWix725xqKHoP5m0-jZXlG5cs8TW-T"),
        ("2️⃣6️⃣ Ilmu Gizi & Kesehatan", "https://www.youtube.com/watch?v=levzTqjwEtk"),
        ("2️⃣7️⃣ Teknologi Masa Depan", "https://www.youtube.com/watch?v=DFCWq868foo"),
        ("2️⃣8️⃣ Tips Belajar Efektif", "https://www.youtube.com/watch?v=JzvMIGPFEqU"),
        ("2️⃣9️⃣ Evolusi Teknologi", "https://www.youtube.com/watch?v=Mee7At7Kvtw"),
        ("3️⃣0️⃣ Ekologi & Lingkungan", "https://www.youtube.com/watch?v=-g-r_pFg8RM"),
        ("3️⃣1️⃣ Sistem Imun Tubuh", "https://www.youtube.com/watch?v=aEqiCz00_Zs"),
        ("3️⃣2️⃣ Sejarah Peradaban Dunia", "https://www.youtube.com/watch?v=Nu16eO1Qu88"),
        ("3️⃣3️⃣ Pengenalan Mikrobiologi", "https://www.youtube.com/watch?v=yDC30CuWI8M"),
        ("3️⃣4️⃣ Filsafat Dasar", "https://www.youtube.com/watch?v=cL7fxbq32S4"),
        ("3️⃣5️⃣ Bahasa Jepang Dasar", "https://www.youtube.com/watch?v=icK6kVTegDA"),
        ("3️⃣6️⃣ Ilmu Data & Statistik", "https://www.youtube.com/watch?v=i32MX8zyQw0"),
        ("3️⃣7️⃣ Proses Pembentukan Batuan", "https://www.youtube.com/watch?v=detbILyfszg"),
        ("3️⃣8️⃣ Dasar Fotografi", "https://www.youtube.com/watch?v=kA1jXBZCHNI"),
        ("3️⃣9️⃣ Sejarah Islam di Nusantara", "https://www.youtube.com/watch?v=wmvk67OoeHY"),
        ("4️⃣0️⃣ Manajemen Waktu Efektif", "https://www.youtube.com/watch?v=P-CS6RVU7ic"),
        ("4️⃣1️⃣ Sejarah Penemuan Listrik", "https://www.youtube.com/watch?v=-8mfKvkCjJ0"),
        ("4️⃣2️⃣ Cara Kerja Mesin Uap dan Revolusi Industri", "https://www.youtube.com/watch?v=z7vDz9YhWN4"),
        ("4️⃣3️⃣ Pengenalan Ilmu Geologi", "https://www.youtube.com/watch?v=llxBAnPKssw"),
        ("4️⃣4️⃣ Belajar Coding dengan Scratch", "https://www.youtube.com/watch?v=Ji_Ncwy8TWM&list=PLk751IW0rPNAlm95zYTns8JkqYSD839d-"),
        ("4️⃣5️⃣ Teknologi Blockchain dan Cryptocurrency", "https://www.youtube.com/watch?v=nTdvZpQKCBU"),
        ("4️⃣6️⃣ Mengenal Sel Hewan dan Tumbuhan", "https://www.youtube.com/watch?v=r9hk9izSJ0c"),
        ("4️⃣7️⃣ Pengenalan Bioteknologi Modern", "https://www.youtube.com/watch?v=dJ8OM4n_XRk"),
        ("4️⃣8️⃣ Strategi Belajar Matematika Cepat", "https://www.youtube.com/watch?v=PEz5e63j0qY"),
        ("4️⃣9️⃣ Sejarah Dunia dalam 10 Menit", "https://www.youtube.com/watch?v=xCeJJglgTU8"),
        ("5️⃣0️⃣ Dasar-Dasar Ekonomi Digital", "https://www.youtube.com/watch?v=wy2C6U3_AbA"),
        ("5️⃣1️⃣ Sejarah Perkembangan Komputer", "https://www.youtube.com/watch?v=k_4DOQbcXmU"),
        ("5️⃣2️⃣ Algoritma dan Logika Pemrograman", "https://www.youtube.com/watch?v=uqVJc9lLknA"),
        ("5️⃣3️⃣ Pengenalan Kecerdasan Buatan", "https://www.youtube.com/watch?v=UYp32dGr5X8"),
        ("5️⃣4️⃣ Machine Learning untuk Pemula", "https://www.youtube.com/watch?v=mEwoAV5_dcA"),
        ("5️⃣5️⃣ Pemrograman Web dengan HTML dan CSS", "https://www.youtube.com/watch?v=NBZ9Ro6UKV8"),
        ("5️⃣6️⃣ Belajar JavaScript Dasar", "https://www.youtube.com/watch?v=mD6uSGSjgr4"),
        ("5️⃣7️⃣ Dasar-Dasar Jaringan Komputer", "https://www.youtube.com/watch?v=BO-QBVB3Glc&list=PLbLqbqNn7VYpEBDzGnbsNwm_I15GUrx45"),
        ("5️⃣8️⃣ Cyber Security untuk Pemula", "https://www.youtube.com/watch?v=BYzNxcPbz1o&list=PLbLqbqNn7VYpxKV_tIgbpb3WvZeY9BfXE"),
        ("5️⃣9️⃣ Pengenalan Cloud Computing", "https://www.youtube.com/watch?v=iw3pCL8UiX8"),
        ("6️⃣0️⃣ Database dan SQL Dasar", "https://www.youtube.com/watch?v=OfrTiLzHv3g&list=PLTbTZ9z52SzMi5EmUGqVceaIVGuk426on"),
        ("6️⃣1️⃣ DevOps: Apa Itu dan Bagaimana Cara Kerjanya?", "https://www.youtube.com/watch?v=zG1cM9VSINg"),
        ("6️⃣2️⃣ Dasar Git dan Version Control", "https://www.youtube.com/watch?v=fQbTeNX1mvM&t=92s"),
        ("6️⃣3️⃣ Pemrograman Python Lanjutan", "https://www.youtube.com/watch?v=iA8lLwmtKQM&list=PLZS-MHyEIRo59lUBwU-XHH7Ymmb04ffOY"),
        ("6️⃣4️⃣ Data Science: Konsep Dasar", "https://www.youtube.com/watch?v=d6xiqfpXAU8"),
        ("6️⃣5️⃣ Internet of Things (IoT) untuk Pemula", "https://www.youtube.com/watch?v=o44PHBZ3uI4&list=PLF1krL_nkpHjnXb51rbeVkHfBglRbsrvP"),
    ]

    for title, url in video_list:
        video_block(title, url)


# Footer
st.markdown(
    """
    <hr style="margin-top: 50px; margin-bottom: 10px;">
    <div style='text-align: center; color: grey;'>
        © 2025 Ilhamdi Taufik. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)
