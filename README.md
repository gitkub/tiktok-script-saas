# TikTok Script Generator API

A standalone FastAPI application that generates TikTok scripts from video transcripts using Apify and OpenAI.

## Features

- Extract transcripts from TikTok videos using Apify
- Generate 4 unique TikTok scripts based on the original video's style and content
- RESTful API with automatic documentation
- Error handling and validation
- CORS support for web applications

## Installation

1. Clone or copy this folder to your project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` file with your API keys:
   - `APIFY_TOKEN`: Get from [Apify Console](https://console.apify.com/account/integrations)
   - `OPENAI_API_KEY`: Get from [OpenAI Platform](https://platform.openai.com/account/api-keys)

## Usage

### Start the server
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

#### Generate TikTok Scripts
- **URL**: `/api/tiktok/script`
- **Method**: `GET`
- **Query Parameters**:
  - `video_url` (required): TikTok video URL

**Example Request:**
```bash
curl "http://localhost:8000/api/tiktok/script?video_url=https://www.tiktok.com/@username/video/1234567890"
```

**Example Response:**
```json
{
  "success": true,
  "original_transcript": "Original video transcript...",
  "generated_scripts": "{\"script_1\": \"Generated script 1...\", \"script_2\": \"Generated script 2...\", \"script_3\": \"Generated script 3...\", \"script_4\": \"Generated script 4...\"}",
  "video_url": "https://www.tiktok.com/@username/video/1234567890",
  "scripts_count": 4
}
```

#### Health Check
- **URL**: `/health`
- **Method**: `GET`

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

### CORS Settings
By default, CORS is configured to allow all origins. For production, modify the `allow_origins` list in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Apify Actor
The application uses the Apify actor `emQXBCL3xePZYgJyn` for TikTok transcript extraction. This actor ID is hardcoded in the router but can be made configurable if needed.

### OpenAI Model
Currently uses `gpt-4.1-nano` model. You can change this in `routers/tiktok_script.py` if needed.

## Error Handling

The API includes comprehensive error handling for:
- Missing video URL
- Missing environment variables
- Apify API errors
- OpenAI API errors
- Transcript not found
- General server errors

## License

This is extracted code for standalone use. Please ensure you have appropriate licenses for Apify and OpenAI services.

## Requirements

- Python 3.7+
- Apify account and API token
- OpenAI account and API key
- Internet connection for API calls