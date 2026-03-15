# DDG Intelligence API

A standalone Django REST Framework service that leverages DuckDuckGo's AI models for text extraction and intelligence, inspired by the DuckDuckGo-ChatAPI C# implementation.

## Features
-   **Intelligence API**: Extract details from unstructured text.
-   **Zero Local LLM Overhead**: Runs logic in the cloud via DuckDuckGo.
-   **Minimal Footprint**: Lightweight Django service.

## Usage

### 1. Extraction API
**Endpoint**: `POST /api/intelligence/extract/`

**Payload**:
```json
{
  "text": "Hey, I need 2 large pepperoni pizzas and a bottle of Coke delivered to 15 Orchard Road.",
  "details": "items, quantities, and delivery address",
  "model": "gpt-4o-mini"
}
```

### 2. General Chat API
**Endpoint**: `POST /api/intelligence/chat/`

**Payload**:
```json
{
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "model": "gpt-4o-mini"
}
```

## Running Locally
1. Install dependencies: `pip install django djangorestframework requests httpx`
2. Start the server: `python manage.py runserver`
