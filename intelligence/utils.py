import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, model_name="gemini-2.0-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def chat(self, messages, response_json=False, image_data=None):
        """
        Send a chat request to Gemini.
        messages: List of dicts, e.g., [{"role": "user", "content": "Hello"}]
        image_data: Can be a Base64 string, a URL string, or binary bytes
        """
        try:
            history = []
            last_message_parts = []
            
            # 1. Prepare history
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                if msg == messages[-1]:
                    # The last message content is part of the prompt
                    last_message_parts.append(msg["content"])
                else:
                    history.append({"role": role, "parts": [msg["content"]]})

            # 2. Process Image
            if image_data:
                final_bytes = None
                
                # Case A: Binary Bytes (from form-data)
                if isinstance(image_data, bytes):
                    final_bytes = image_data
                
                # Case B: String (URL or Base64)
                elif isinstance(image_data, str) and image_data.strip():
                    if image_data.startswith("http"):
                        import requests
                        final_bytes = requests.get(image_data, timeout=10).content
                    else:
                        import base64
                        # Strip common base64 prefixes if present
                        if "," in image_data:
                            image_data = image_data.split(",")[1]
                        # Remove whitespace/newlines that might break decoding
                        image_data = "".join(image_data.split())
                        final_bytes = base64.b64decode(image_data)

                if final_bytes:
                    # Use PIL to verify image and get correct MIME type
                    from PIL import Image
                    import io
                    img = Image.open(io.BytesIO(final_bytes))
                    mime_type = f"image/{img.format.lower()}"
                    if img.format.lower() == "jpeg": mime_type = "image/jpeg"
                    
                    logger.info(f"Processing image: {img.format} ({len(final_bytes)} bytes)")
                    
                    last_message_parts.append({
                        "mime_type": mime_type,
                        "data": final_bytes
                    })

            # 3. Request Generation
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
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
