from intelligence.utils import GeminiClient
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

def test_gemini():
    print(f"Using API Key: {os.getenv('GEMINI_API_KEY')[:10]}...")
    client = GeminiClient(model_name="gemini-flash-latest")
    messages = [
        {"role": "user", "content": "Extract items and quantities from: 4 red apples and 2 green bananas. Return JSON only."}
    ]
    print("Sending request to Gemini...")
    result = client.chat(messages)
    print("Result:")
    print(result)

if __name__ == "__main__":
    test_gemini()
