from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CodeRequest(BaseModel):
    code: str

@app.post("/review")
def review_code(request: CodeRequest):
    """Review the given code using OpenAI"""
    prompt = f"Review this Python code and suggest improvements:\n\n{request.code}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional code reviewer."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"review": response.choices[0].message.content}
