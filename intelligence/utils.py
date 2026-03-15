import requests
import json
import logging

logger = logging.getLogger(__name__)

class DDGClient:
    MODELS = {
        "gpt-4o-mini": "gpt-4o-mini",
        "llama-3.3-70b": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "claude-3-haiku": "claude-3-haiku-20240307",
        "o3-mini": "o3-mini",
        "mixtral-8x7b": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    }

    def __init__(self, model="gpt-4o-mini"):
        self.model = self.MODELS.get(model, model)
        self.vqd_token = None
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        })

    def _get_vqd(self):
        """Obtain the initial X-Vqd-4 token."""
        headers = {"X-Vqd-Accept": "1"}
        try:
            # First, hit the main page to set any cookies if needed (like the C# code does)
            self.session.get("https://duckduckgo.com/?q=DuckDuckGo+AI+Chat&ia=chat&duckai=1")
            
            # Then get the status/token
            response = self.session.get("https://duckduckgo.com/duckchat/v1/status", headers=headers)
            response.raise_for_status()
            self.vqd_token = response.headers.get("x-vqd-4")
            return self.vqd_token
        except Exception as e:
            logger.error(f"Failed to initialize VQD token: {e}")
            return None

    def chat(self, messages):
        """
        Send a chat request.
        messages: List of dicts, e.g., [{"role": "user", "content": "Hello"}]
        """
        if not self.vqd_token:
            if not self._get_vqd():
                return {"error": "Could not initialize session"}

        payload = {
            "model": self.model,
            "messages": messages
        }

        headers = {
            "Content-Type": "application/json",
            "x-vqd-4": self.vqd_token
        }

        try:
            response = self.session.post(
                "https://duckduckgo.com/duckchat/v1/chat",
                headers=headers,
                json=payload,
                stream=True
            )
            response.raise_for_status()

            # Update the VQD token for the next message in the conversation
            self.vqd_token = response.headers.get("x-vqd-4")

            full_content = []
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: "):
                        data_str = decoded_line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            data_json = json.loads(data_str)
                            if "message" in data_json:
                                full_content.append(data_json["message"])
                        except json.JSONDecodeError:
                            continue

            return {"content": "".join(full_content)}

        except Exception as e:
            logger.error(f"Chat request failed: {e}")
            return {"error": str(e)}
