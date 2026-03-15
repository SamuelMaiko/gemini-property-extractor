# 🧠 Gemini Intelligence API (Multimodal)

A standalone, high-performance API service built with **Django REST Framework** to provide AI-powered text extraction and chat capabilities. Powered by **Google Gemini 1.5 Flash**, it is highly stable, multimodal (supports vision), and cost-effective.

## 🚀 Key Features
- **Data Extraction**: Extract structured JSON from raw text or images (Receipts, IDs, Notes, etc.)
- **Vision Support**: Analyze images via URL, Base64 strings, or direct File uploads.
- **Multimodal Chat**: Full conversation support with image context.
- **Usage Metadata**: Every response includes precise token consumption data.

## 🛠️ Setup & Installation

1. **Clone the repository** (if you haven't already).
2. **Install Dependencies**:
   ```bash
   pip install django djangorestframework google-generativeai python-dotenv Pillow django-cors-headers requests
   ```
3. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_key
   ```
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

Extracts specific details from text or images and returns **clean JSON**.

**Payload (JSON)**:
```json
{
  "text": "Please bring 5 blue pens to the main office",
  "details": "item, quantity, color, and destination",
  "image": "optional_base64_or_url"
}
```

**CURL Example (Form-Data / Image Upload)**:
```bash
curl -X POST "http://localhost:8040/api/intelligence/extract/" \
     -F "text=Extract details from this receipt" \
     -F "details=total, date, merchant" \
     -F "image=@receipt.jpg"
```

### 2. General Chat
**Endpoint**: `POST /api/intelligence/chat/`

General reasoning and chat interface.

**Payload**:
```json
{
  "messages": [
    {"role": "user", "content": "What is in this picture?"}
  ],
  "image": "https://example.com/photo.png"
}
```

## 📊 Token Usage Response
Every response follows this structure:
```json
{
  "content": { ... },
  "usage": {
    "prompt_tokens": 54,
    "candidates_tokens": 29,
    "total_tokens": 83
  }
}
```

## 📝 License
MIT
