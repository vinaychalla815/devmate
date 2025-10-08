from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
from app.memory_manager import summarize_code, store_summary
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
    """Review the given code using OpenAI (v2.1.0 syntax)"""
    prompt = f"Review this Python code and suggest improvements:\n\n{request.code}"

    try:
        # ✅ Correct call for OpenAI v2.x
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )

        review_text = response.output[0].content[0].text

        # ✅ Summarize and store memory (optional)
        summary = summarize_code(request.code)
        store_summary("reviewed_code.py", summary)

        return {"review": review_text}

    except Exception as e:
        # 👇 This will show clear errors instead of "Internal Server Error"
        return {"error": str(e)}


# --- 2. /testgen endpoint ---
@router.post("/testgen")
def generate_tests(request: CodeRequest):
    """Generate clean Python unit test code using pytest"""
    prompt = f"Generate only the Python pytest code (no explanations) for the following function:\n\n{request.code}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert Python test generator. Return only code, no explanations."},
            {"role": "user", "content": prompt}
        ]
    )

    clean_output = response.choices[0].message.content.strip("`python").strip("`").strip()
    return {"tests": clean_output}
   

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
