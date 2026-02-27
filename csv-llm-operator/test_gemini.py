import requests
import json
import os

API_KEY = os.getenv("GEMINI_API_KEY")

# モデル名を一覧にあった「gemini-flash-latest」に変更
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={API_KEY}"

headers = {'Content-Type': 'application/json'}
data = {
    "contents": [{
        "parts": [{"text": "接続テスト成功！と叫んでください。"}]
    }]
}

print("Geminiにリクエスト送信中（モデル: gemini-flash-latest）...")
response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    answer = result['candidates'][0]['content']['parts'][0]['text']
    print("-" * 30)
    print("Geminiの回答:", answer)
    print("-" * 30)
else:
    print(f"ステータスコード: {response.status_code}")
    print("エラー内容:", response.text)