import os 
import requests 
from dotenv import load_dotenv

load_dotenv()

api_key =os.getenv("GROQ_API_KEY")

response = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)

print("Status Code:", response.status_code)

if response.ok:
    models = response.json()
    models = models["data"]

for model in models:
    print(model["id"])

else:
    print(response.text)