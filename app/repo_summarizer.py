from github import Github
from openai import OpenAI
import os, json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_all_files(repo, path=""):
    """Recursively collect all .py files in the repo."""
    items = repo.get_contents(path)
    files = []
    for item in items:
        if item.type == "file" and item.path.endswith(".py"):
            files.append(item)
        elif item.type == "dir":
            files.extend(get_all_files(repo, item.path))
    return files

def summarize_repo(repo_name: str):
    """Fetch all Python files, summarize them, and store in /memory/repo_summary.json."""
    token = os.getenv("GITHUB_TOKEN")
    g = Github(token)
    repo = g.get_repo(repo_name)

    summaries = {}
    files = get_all_files(repo)

    for content_file in files:
        code = content_file.decoded_content.decode("utf-8")
        prompt = f"Summarize the purpose and key functions of this Python file:\n\n{code[:4000]}"

        try:
            response = client.responses.create(
                model="gpt-4o-mini",
                input=prompt
            )
            summary = response.output_text
        except Exception as e:
            summary = f"Error summarizing file: {e}"

        summaries[content_file.path] = summary

    os.makedirs("memory", exist_ok=True)
    with open("memory/repo_summary.json", "w") as f:
        json.dump(summaries, f, indent=2)

    return {"status": "Summaries generated", "files": list(summaries.keys())}
