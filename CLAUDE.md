# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
# Start the server (development)
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup
Required environment variables in `.env` file:
- `APIFY_TOKEN`: Get from Apify Console
- `OPENAI_API_KEY`: Get from OpenAI Platform

### Deployment Notes
For Render deployment issues with pydantic-core compilation:
- Use updated dependencies in requirements.txt (includes newer pydantic version)
- Fallback option: Use requirements-fallback.txt if build issues persist

## Architecture Overview

This is a FastAPI-based TikTok script generator that integrates two external services:

### Core Components
- **main.py**: FastAPI application entry point with CORS middleware and basic routing
- **routers/tiktok_script.py**: Main business logic router handling the script generation workflow

### Service Integration Pattern
The application follows a two-step AI pipeline:
1. **Transcript Extraction**: Uses Apify client with actor `emQXBCL3xePZYgJyn` to extract transcripts from TikTok videos
2. **Script Generation**: Uses OpenAI GPT-4o-mini to generate 4 unique Thai-language TikTok scripts based on the original transcript's style

### API Structure
- Single primary endpoint: `GET /api/tiktok/script?video_url=<url>`
- Health check endpoint: `GET /health`
- Root endpoint: `GET /` (provides API overview)

### Key Implementation Details
- Thai language prompts and responses in OpenAI integration
- Hardcoded Apify actor ID for TikTok transcript extraction
- JSON response format with 4 generated scripts
- Comprehensive error handling for missing environment variables, API failures, and missing transcripts
- CORS configured for all origins (modify for production)

### Error Handling Strategy
The router implements layered error handling:
- Input validation (video URL presence)
- Environment variable validation (API keys)
- External service error handling (Apify, OpenAI)
- Generic exception catching with detailed error messages

### Dependencies
External services: Apify (transcript extraction), OpenAI (script generation)
Key packages: fastapi, apify-client, openai, python-dotenv