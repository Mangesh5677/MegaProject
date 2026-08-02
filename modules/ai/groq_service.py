import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


SYSTEM_PROMPT = """
You are an AI Productivity Assistant.

Your job is to help students manage:

• Tasks
• Deadlines
• Fixed Timetable
• Study Planning
• Productivity
• Time Management

Rules:

1. Always prioritize HIGH priority tasks.
2. If deadlines are close, mention them.
3. Suggest practical study plans.
4. Keep answers concise.
5. Use bullet points whenever possible.
6. Encourage productive habits.
7. Never invent tasks or timetable events.
"""


def ask_ai(context, question):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },

            {
                "role": "user",
                "content": f"""
User Data

{context}

Question

{question}
"""
            }
        ],

        temperature=0.4,

        max_tokens=700,

        top_p=1,

        stream=False,
    )

    return response.choices[0].message.content.strip()