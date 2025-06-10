import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_BASE_URL = "https://api.groq.com"
GROQ_API_VERSION = "openai/v1"
GROQ_CHAT_ENDPOINT = "/chat/completions"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

class LLMWrapper:
    def __init__(self, base_url: str = GROQ_API_BASE_URL, api_version: str = GROQ_API_VERSION):
        self.base_url = base_url
        self.api_version = api_version

    def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        url = f"{self.base_url}/{self.api_version}{GROQ_CHAT_ENDPOINT}"

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature":0.0
            # Add temperature, stop, etc., if needed
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            if response.status_code == 401:
                raise RuntimeError("Authentication error: Invalid API key")
            else:
                raise RuntimeError(f"Inference API error {response.status_code}: {response.text}")

        data = response.json()
        generated_text = data["choices"][0]["message"]["content"]
        return generated_text.strip()

