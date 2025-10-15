import requests
from typing import List, Dict
from app.config import settings


class OllamaService:
    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = settings.OLLAMA_MODEL

    def chat(self, messages: List[Dict[str, str]]) -> str:
        try:
            if not any(msg.get("role") == "system" for msg in messages):
                messages.insert(
                    0,
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Keep your responses concise and brief, ideally under 50 words.",
                    },
                )
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "num_predict": 50,
                    },
                },
            )

            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.status_code}")

            return response.json()["message"]["content"]

        except requests.RequestException as e:
            raise Exception(f"Failed to connect to Ollama: {str(e)}")
