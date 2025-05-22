import os
from openai import OpenAI
import subprocess
import requests

# Get PR info from GitHub Actions env
pr_number = os.getenv("PR_NUMBER")
repo = os.getenv("GITHUB_REPOSITORY")
token = os.getenv("GITHUB_TOKEN")

# Get diff using git CLI
diff = subprocess.check_output(["git", "diff", "origin/main...HEAD"], text=True)

# Call ChatGPT
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {
        "role": "system",
        "content": (
                    "You are a senior software engineer and an expert code reviewer. "
                    "When provided with code diffs, you will perform a detailed and structured review. "
                    "Break your feedback into the following sections:"
                    "1. Summary of Code Changes – Describe in simple terms what the changes are trying to do."
                    "2. Code Quality Issues – Point out bugs, code smells, or inefficiencies."
                    "3. Suggestions for Improvement – Offer clear, better alternatives (with code snippets) for problematic parts."
                    "4. Overall Assessment – Summarize how good or bad the changes are and if they meet clean code standards."
                    "Be constructive, concise, and professional."
        )
    },
    {
        "role": "user",
        "content": f"Here is the code diff:\n\n{diff}"
    }
]
)
review_comment = response.choices[0].message.content

# Post comment to PR
url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
headers = {"Authorization": f"token {token}"}
requests.post(url, json={"body": review_comment}, headers=headers)
