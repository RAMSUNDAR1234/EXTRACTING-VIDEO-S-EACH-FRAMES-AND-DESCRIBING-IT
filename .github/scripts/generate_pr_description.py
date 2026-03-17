import os
import json
import urllib.request

api_key = os.environ['JUSPAY_API_KEY']
pr_title = os.environ.get('PR_TITLE', '')
pr_branch = os.environ.get('PR_BRANCH', '')
base_branch = os.environ.get('BASE_BRANCH', '')
added = os.environ.get('ADDED', '0')
modified = os.environ.get('MODIFIED', '0')
deleted = os.environ.get('DELETED', '0')

with open('/tmp/commits.txt', 'r') as f:
    commits = f.read()

with open('/tmp/files.txt', 'r') as f:
    files = f.read()

prompt = f"""You are a senior software engineer reviewing a pull request. Generate a comprehensive PR description.

PR Title: {pr_title}
Branch: {pr_branch} -> {base_branch}

Changed Files: {added} added, {modified} modified, {deleted} deleted

Commits:
{commits}

Files:
{files}

Generate PR description with: Summary, Changes Made, Files Changed, Impact Assessment, Testing, Checklist.
Format as clean Markdown."""

data = {
    "model": "open-large",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant that generates clear, concise pull request descriptions."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.3,
    "max_tokens": 2000
}

req = urllib.request.Request(
    "https://grid.ai.juspay.net/v1/chat/completions",
    data=json.dumps(data).encode(),
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
        description = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        if not description:
            raise Exception("Empty response")
except Exception as e:
    description = f"## Summary\nThis PR includes changes to {modified} files.\n\n## Changes\n{commits}\n\n*AI unavailable: {str(e)}*"

with open('/tmp/ai_description.txt', 'w') as f:
    f.write(description)
