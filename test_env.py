from dotenv import load_dotenv
import os

load_dotenv()

print("GMAIL_EMAIL:", os.getenv("GMAIL_EMAIL"))
print("GMAIL_APP_PASSWORD:", os.getenv("GMAIL_APP_PASSWORD"))