from fastapi import APIRouter
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

@router.post("/review")
def review_code():
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful code reviewer."},
                {"role": "user", "content": "Review this Python code:\nprint('Hello, World!')"}
            ]
        )
        return {"review": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

@router.post("/testgen")
def generate_tests():
    return {"tests": "This is a dummy test generation response."}

@router.post("/docupdate")
def update_docs():
    return {"docs": "This is a dummy documentation update response."}
   

