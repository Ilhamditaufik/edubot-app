import random

def get_question(level):
    questions = {
        "Mudah": [
            {"question": "Apa ibukota Indonesia?", "answer": "Jakarta"},
            {"question": "Berapa hasil dari 2 + 2?", "answer": "4"},
            {"question": "Warna bendera Indonesia?", "answer": "Merah Putih"},
            {"question": "Siapa presiden pertama Indonesia?", "answer": "Soekarno"},
            {"question": "Hewan berkaki delapan disebut?", "answer": "Laba-laba"},
            {"question": "Berapakah jumlah hari dalam seminggu?", "answer": "7"},
            {"question": "Planet ketiga dari Matahari?", "answer": "Bumi"},
            {"question": "Alat untuk menulis di papan tulis?", "answer": "Spidol"},
            {"question": "Satuan ukuran panjang?", "answer": "Meter"},
            {"question": "Air membeku pada suhu?", "answer": "0"}
        ],
        "Sedang": [
            {"question": "Siapa penemu lampu pijar?", "answer": "Thomas Edison"},
            {"question": "Hasil dari 12 x 12?", "answer": "144"},
            {"question": "Gunung tertinggi di dunia?", "answer": "Everest"},
            {"question": "Organ yang memompa darah?", "answer": "Jantung"},
            {"question": "Ibu kota negara Thailand?", "answer": "Bangkok"},
            {"question": "Hewan tercepat di darat?", "answer": "Cheetah"},
            {"question": "Nama unsur kimia dengan simbol O?", "answer": "Oksigen"},
            {"question": "Penulis Romeo and Juliet?", "answer": "Shakespeare"},
            {"question": "Planet terbesar di tata surya?", "answer": "Jupiter"},
            {"question": "Sungai terpanjang di dunia?", "answer": "Nile"}
        ],
        "Sulit": [
            {"question": "Apa nama ibu kota Kazakhstan?", "answer": "Astana"},
            {"question": "Siapa ilmuwan teori relativitas?", "answer": "Einstein"},
            {"question": "Bahasa resmi Brazil?", "answer": "Portugis"},
            {"question": "Berapakah akar kuadrat dari 625?", "answer": "25"},
            {"question": "Tahun Proklamasi Kemerdekaan Indonesia?", "answer": "1945"},
            {"question": "Gunung tertinggi di Indonesia?", "answer": "Puncak Jaya"},
            {"question": "Simbol kimia dari Emas?", "answer": "Au"},
            {"question": "Planet dengan cincin terbesar?", "answer": "Saturnus"},
            {"question": "Nama zat yang membuat daun hijau?", "answer": "Klorofil"},
            {"question": "Penemu teori evolusi?", "answer": "Charles Darwin"}
        ]
    }
    # Ambil pertanyaan acak
    return random.choice(questions[level])
