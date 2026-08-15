import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def extract_skills(resume_text: str) -> list[str]:
    response = client.chat.completions.create(
        model="gemini-3.6-flash",
        messages=[
            {
                "role": "user",
                "content": f"Extract only the technical skills from this resume as a comma-separated list, nothing else, no explanation:\n\n{resume_text}"
            }
        ]
    )
    raw = response.choices[0].message.content
    skills = [s.strip() for s in raw.split(",") if s.strip()]
    return skills