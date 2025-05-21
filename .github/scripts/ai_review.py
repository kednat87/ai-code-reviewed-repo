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
                    "You are a senior SQL expert and code reviewer. "
                    "When given a SQL query, provide a detailed and structured review focusing only on the SQL logic. "
                    "Break your feedback into the following sections:"
                    "1. SQL Issues Identified - List any logic errors, performance bottlenecks, poor formatting, or bad practices."
                    "2. Suggested Fixes - Provide the corrected SQL query, with improvements for readability, logic correctness, or efficiency."
                    "3. Brief Explanation - Explain why the original query needed changes and what the new version improves."
                    "Be concise, clear, and assume the reviewer has working SQL knowledge."
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
