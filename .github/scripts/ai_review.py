import os
import openai
import subprocess
import requests

# Get PR info from GitHub Actions env
pr_number = os.getenv("GITHUB_REF").split("/")[-1]
repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("GITHUB_TOKEN")

# Get diff using git CLI
diff = subprocess.check_output(["git", "diff", "origin/main...HEAD"], text=True)

# Call ChatGPT
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{
        "role": "user",
        "content": f"Review the following pull request diff and provide constructive feedback:\n\n{diff}"
    }],
    max_tokens=500
)
review_comment = response['choices'][0]['message']['content']

# Post comment to PR
url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
headers = {"Authorization": f"token {token}"}
requests.post(url, json={"body": review_comment}, headers=headers)
