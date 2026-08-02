import os
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("GMAIL_EMAIL")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def send_email(receiver, subject, body):
    """
    Send an email using Gmail SMTP.
    """

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            server.login(EMAIL, PASSWORD)

            server.send_message(msg)

        print("✅ Email Sent Successfully")

    except Exception as e:
        print("❌ Failed to send email")
        print(e)