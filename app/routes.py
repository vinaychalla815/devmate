from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

# --- Request schema ---
class CodeRequest(BaseModel):
    code: str

# --- 1. /review endpoint ---
@router.post("/review")
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


# --- 2. /testgen endpoint ---
@router.post("/testgen")
def generate_tests(request: CodeRequest):
    """Generate test cases for the given code"""
    prompt = f"Generate Python unit test cases for the following code using pytest:\n\n{request.code}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert Python test generator."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"tests": response.choices[0].message.content}
   

# --- 3. /docupdate endpoint ---
@router.post("/docupdate")
def update_docs(request: CodeRequest):
    """Generate or improve docstrings and comments for the given code"""
    prompt = f"Add or improve Python docstrings and inline comments for the following code:\n\n{request.code}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert software documentation writer."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"documentation": response.choices[0].message.content}
