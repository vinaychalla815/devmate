from github import Github
import os

def list_repo_files(repo_name: str):
    """List top-level files in a GitHub repository."""
    token = os.getenv("GITHUB_TOKEN")
    g = Github(token)
    repo = g.get_repo(repo_name)
    files = [content.path for content in repo.get_contents("")]
    return files
