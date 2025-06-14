import openai

# Ganti dengan API key kamu
openai.api_key = "your_openai_api_key"

def get_bot_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # bisa pakai gpt-4 jika ada
            messages=[
                {"role": "system", "content": "Kamu adalah asisten edukasi yang ramah dan membantu."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Terjadi kesalahan: {e}"
