import os
from openai import OpenAI
import subprocess
import requests

# Get PR info from GitHub Actions env
pr_number = os.getenv("GITHUB_REF").split("/")[-1]
repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("GITHUB_TOKEN")

# Get diff using git CLI
diff = subprocess.check_output(["git", "diff", "origin/main...HEAD"], text=True)

# Call ChatGPT
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a code reviewer..."},
        {"role": "user", "content": diff}
    ]
)
review_comment = response.choices[0].message.content

# Post comment to PR
url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
headers = {"Authorization": f"token {token}"}
requests.post(url, json={"body": review_comment}, headers=headers)
