from dotenv import load_dotenv
import os

load_dotenv()
print("API KEY:", os.getenv("TOGETHER_API_KEY"))
