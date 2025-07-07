
> *"Alhamdulillah berhasil...
Karena sesungguhnya proses itu berasal dari kemauan yang tinggi. 
Kalau aku tidak gigih, mungkin proyek interaktif ini tidak akan pernah ada."*  
 — Ilhamdi Taufik.

---

🎓 Edubot - Aplikasi Edukasi Interaktif
Edubot adalah proyek aplikasi edukasi interaktif berbasis Python & Streamlit yang saya kembangkan untuk membantu pengguna belajar secara menyenangkan. Aplikasi ini dilengkapi chatbot edukatif, kuis interaktif, video pembelajaran, dan sertifikat otomatis. aplikasi edukatif berbasis Python dan Streamlit yang saya kembangkan sebagai media pembelajaran interaktif. Proyek ini merupakan hasil semangat belajar, eksplorasi, dan keinginan kuat untuk berbagi pengetahuan lewat teknologi.

✨ Fitur Utama
🎤 Chatbot Edukatif
Pengguna dapat bertanya materi edukasi, dan chatbot akan menjawab secara interaktif.

🧠 Kuis Interaktif
Tersedia kuis dengan beberapa tingkatan kesulitan yang dapat dipilih.

📹 Video Pembelajaran
Materi edukasi dalam bentuk video untuk memudahkan pemahaman.

🏆 Sertifikat Otomatis
Setelah menyelesaikan kuis, pengguna bisa mendapatkan sertifikat PDF.

🎨 Tampilan Menarik
Desain responsif dengan sidebar dan tema warna.

🚀 Perjalanan Pengembangan
Proyek ini saya bangun tahap demi tahap:
✅ Membuat struktur folder assets, output, dan file app.py, chatbot.py, quiz_data.py.
✅ Membuat tampilan antarmuka menggunakan Streamlit.
✅ Menyiapkan file gambar/logo (logo.webp, logo2.webp, dll) dan memperbaiki error path saat deploy.
✅ Menguji jalannya aplikasi secara lokal di localhost.
✅ Membuat repository GitHub: edubot-app
✅ Push semua source code & update commit.
✅ Deploy aplikasi agar bisa diakses melalui link publik Streamlit.

Proses pengembangan tidak selalu mulus — sempat mengalami error MediaFileStorageError saat gambar tidak ditemukan di folder assets. Masalah tersebut berhasil diperbaiki dengan memastikan struktur direktori sudah sesuai dan semua file ter-push ke GitHub.

⚙️ Cara Menjalankan
Clone repository:

bash
Salin
Edit
git clone https://github.com/Ilhamditaufik/edubot-app.git
cd edubot-app
Install dependency:

nginx
Salin
Edit
pip install -r requirements.txt
Jalankan aplikasi:

arduino
Salin
Edit
streamlit run app.py
🌐 Deploy
Aplikasi ini juga dapat di-deploy di Streamlit Cloud agar publik bisa mengaksesnya melalui link.

📂 Struktur Folder
lua
Salin
Edit
edubot-app/
  ├── assets/
  ├── output/
  ├── app.py
  ├── chatbot.py
  ├── quiz_data.py
  ├── history.json
  ├── requirements.txt
  ├── sertifikat.pdf
💡 Catatan
Proyek ini adalah latihan dan pembuktian proses belajar membangun aplikasi edukasi dari nol hingga bisa digunakan orang lain.
