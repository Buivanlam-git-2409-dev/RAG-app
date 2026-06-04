import requests

api_key = "your_groq_api_key"
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)

print(response.status_code)
print(response.json())
