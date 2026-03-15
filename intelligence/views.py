from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import DDGClient

class ExtractionView(APIView):
    """
    API endpoint to extract specific details from a text message.
    """
    def post(self, request):
        text = request.data.get("text")
        details = request.data.get("details", "important information")
        model = request.data.get("model", "gemini-2.5-flash-lite")

        if not text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

        client = DDGClient(model_name=model)
        
        # Construct the extraction prompt
        system_prompt = f"You are an expert data extractor. Extract the following details from the text: {details}. Return the results ONLY as a clean JSON object. Do not include any explanations or other text."
        
        messages = [
            {"role": "user", "content": f"{system_prompt}\n\nText: {text}"}
        ]
        
        result = client.chat(messages)
        
        if "error" in result:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(result, status=status.HTTP_200_OK)

class ChatView(APIView):
    """
    General chat endpoint.
    """
    def post(self, request):
        messages = request.data.get("messages")
        model = request.data.get("model", "gemini-2.5-flash-lite")

        if not messages or not isinstance(messages, list):
            return Response({"error": "Messages must be a list of dictionaries"}, status=status.HTTP_400_BAD_REQUEST)

        client = DDGClient(model_name=model)
        result = client.chat(messages)
        
        if "error" in result:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(result, status=status.HTTP_200_OK)
