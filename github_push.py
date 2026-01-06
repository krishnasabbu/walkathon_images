import base64
import json
import requests
from pathlib import Path

GITHUB_TOKEN = ""
OWNER = "krishnasabbu"
REPO = "fitness-challenge"
BRANCH = "main"
FILE_PATH = "data/leaderboard.xlsx"   # path inside repo
LOCAL_FILE = "leaderboard.xlsx"

def get_file_sha():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()["sha"]
    return None

def push_excel_to_github():
    content = base64.b64encode(Path(LOCAL_FILE).read_bytes()).decode()

    payload = {
        "message": "Auto update leaderboard",
        "content": content,
        "branch": BRANCH
    }

    sha = get_file_sha()
    if sha:
        payload["sha"] = sha

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.put(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    print("✅ Excel pushed to GitHub successfully")
