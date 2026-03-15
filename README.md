# 🧠 Gemini Property Extractor

A standalone, high-performance API service built with **Django REST Framework** to provide AI-powered text extraction and chat capabilities. Powered by **Google Gemini 1.5 Flash**, it is highly stable, multimodal (supports vision), and cost-effective.

## 🚀 Key Features
- **Data Extraction**: Extract structured JSON from raw text or images (Receipts, IDs, Notes, etc.)
- **Vision Support**: Analyze images via URL, Base64 strings, or direct File uploads.
- **Multimodal Chat**: Full conversation support with image context.
- **Usage Metadata**: Every response includes precise token consumption data.

## 🛠️ Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd gemini-property-extractor
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   Copy the example environment file and replace the placeholder with your actual Gemini API key:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and set your key:
   `GEMINI_API_KEY=your_actual_key_here`
4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Start the Server**:
   ```bash
   python manage.py runserver 8040
   ```

## 📡 API Endpoints

### 1. Data Extraction
**Endpoint**: `POST /api/intelligence/extract/`

Extracts specific details and returns **clean JSON objects**. This endpoint is fully multimodal—it can process text, images, or both simultaneously.

#### A. Text-Only Extraction
Use this when you have a text report (e.g., from a chat message).

**Request**:
```json
{
  "text": "Lost a black leather wallet at the main cafeteria around 2 PM",
  "details": "item_type, color, material, location, approximate_time"
}
```
**Response**:
```json
{
  "content": {
    "item_type": "wallet",
    "color": "black",
    "material": "leather",
    "location": "main cafeteria",
    "approximate_time": "2:00 PM"
  },
  "usage": { "prompt_tokens": 58, "candidates_tokens": 42, "total_tokens": 100 }
}
```

#### B. Image-Only Extraction
Use this when you have a photo (e.g., a found item) but no accompanying text.

**Request**:
```json
{
  "text": "Identify the object and its features",
  "details": "object_name, color, distinctive_marks",
  "image": "https://example.com/found-bag.jpg"
}
```
**Response**:
```json
{
  "content": {
    "object_name": "Backpack",
    "color": "Red",
    "distinctive_marks": "White star logo on the front pocket"
  },
  "usage": { "prompt_tokens": 1050, "candidates_tokens": 35, "total_tokens": 1085 }
}
```

#### C. Multimodal: Image + Caption (Recommended)
Use this when a user sends a photo with a caption. The AI uses both to improve accuracy.

**Request**:
```json
{
  "text": "Found this near the parking lot entrance today",
  "details": "object, location, condition",
  "image": "base64_encoded_string_here"
}
```
**Response**:
```json
{
  "content": {
    "object": "Car keys (Toyota)",
    "location": "Parking lot entrance",
    "condition": "Scratched, attached to a blue keychain"
  },
  "usage": { "prompt_tokens": 1080, "candidates_tokens": 38, "total_tokens": 1118 }
}
```

### 2. General Chat
**Endpoint**: `POST /api/intelligence/chat/`
Used for generating natural language responses back to the user.

**Request**:
```json
{
  "messages": [
    {"role": "user", "content": "Generate a friendly support message for a user who reported a lost Red Backpack."}
  ]
}
```
**Response**:
```json
{
  "content": "Oh no! I've officially logged your Red Backpack report. I'll keep a close eye on the listings and alert you the second a match is found! 🕵️‍♂️",
  "usage": { "prompt_tokens": 40, "candidates_tokens": 45, "total_tokens": 85 }
}
```

## 📊 Token Usage Response
Every response includes a `usage` block. On the **Free Tier (Gemini 1.5 Flash)**, you have a limit of **1,500 requests per day**.

## 📝 License
This project is licensed under the [MIT License](LICENSE).
