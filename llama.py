import requests
from dotenv import load_dotenv
import os 

load_dotenv()

api_token = os.getenv("HF_API_TOKEN")
if not api_token:
    raise ValueError("API token is not set. Please check your .env file.")

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B"
headers = {"Authorization": f"Bearer {api_token}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	print(response.json())
	return response.json()
	
output = query({
	"inputs": "Can you please let us know more details about your ",
})