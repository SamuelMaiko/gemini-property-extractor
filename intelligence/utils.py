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

    def chat(self, messages, response_json=False, image_base64=None):
        """
        Send a chat request to Gemini.
        messages: List of dicts, e.g., [{"role": "user", "content": "Hello"}]
        image_base64: Optional base64 encoded image string
        """
        try:
            history = []
            last_message_parts = []
            
            # Handle messages history
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                if msg == messages[-1]:
                    last_message_parts.append(msg["content"])
                else:
                    history.append({"role": role, "parts": [msg["content"]]})

            # Add image to the last user message if provided
            if image_base64:
                import base64
                image_data = base64.b64decode(image_base64)
                last_message_parts.append({
                    "mime_type": "image/jpeg", # Defaulting to jpeg, Gemini handles most
                    "data": image_data
                })

            generation_config = {}
            if response_json:
                generation_config["response_mime_type"] = "application/json"

            chat_session = self.model.start_chat(history=history)
            response = chat_session.send_message(
                last_message_parts, 
                generation_config=generation_config
            )
            
            return {
                "content": response.text,
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count,
                    "candidates_tokens": response.usage_metadata.candidates_token_count,
                    "total_tokens": response.usage_metadata.total_token_count,
                }
            }

        except Exception as e:
            logger.error(f"Gemini request failed: {e}")
            return {"error": str(e)}

# Alias for backward compatibility in views
DDGClient = GeminiClient
