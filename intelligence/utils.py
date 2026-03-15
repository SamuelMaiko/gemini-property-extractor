import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, model_name="gemini-2.5-flash-lite"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def chat(self, messages):
        """
        Send a chat request to Gemini.
        messages: List of dicts, e.g., [{"role": "user", "content": "Hello"}]
        """
        try:
            history = []
            last_message = ""
            
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                if msg == messages[-1]:
                    last_message = msg["content"]
                else:
                    history.append({"role": role, "parts": [msg["content"]]})

            chat_session = self.model.start_chat(history=history)
            response = chat_session.send_message(last_message)
            
            return {"content": response.text}

        except Exception as e:
            logger.error(f"Gemini request failed: {e}")
            return {"error": str(e)}

# Alias for backward compatibility in views
DDGClient = GeminiClient
