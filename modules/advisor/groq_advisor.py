import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Add it to .env or Streamlit Secrets.")

client = Groq(api_key=api_key)


def get_ai_advice(tasks, timetable):

    prompt = f"""
You are an AI Productivity Coach.

Today's Fixed Timetable:
{timetable}

Pending Tasks:
{tasks}

Give:
1. Best order of tasks
2. Which task should be completed first
3. Time management tips
4. Motivation

Keep the answer under 200 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content