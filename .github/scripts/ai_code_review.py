import os
import json
import urllib.request

api_key = os.environ['JUSPAY_API_KEY']
pr_title = os.environ.get('PR_TITLE', '')
pr_body = os.environ.get('PR_BODY', '')
files = os.environ.get('FILES', '')
diff_stat = os.environ.get('DIFF_STAT', '')

with open('/tmp/pr_diff.txt', 'r') as f:
    diff_content = f.read()[:15000]

prompt = f"""You are an expert senior software engineer conducting a thorough code review.

PR Title: {pr_title}
PR Description: {pr_body}

Diff Statistics:
{diff_stat}

Changed Files:
{files}

Code Diff (first 15KB):
{diff_content}

Provide structured code review with:
## Overall Assessment
## Code Quality
## Best Practices
## Potential Issues
## Suggestions
## Testing

Format in Markdown."""

data = {
    "model": "open-large",
    "messages": [
        {"role": "system", "content": "You are an expert senior software engineer. Provide actionable code review feedback."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.2,
    "max_tokens": 3000
}

req = urllib.request.Request(
    'https://grid.ai.juspay.net/v1/chat/completions',
    data=json.dumps(data).encode(),
    headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
        review = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        if not review:
            raise Exception('Empty response')
except Exception as e:
    review = f'## AI Review\n\nUnable to generate AI review: {str(e)}\n\n**Diff Stats:**\n```\n{diff_stat}\n```'

with open('/tmp/ai_review.txt', 'w') as f:
    f.write(review)
