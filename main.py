from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tiktok_script

# Create FastAPI app
app = FastAPI(
    title="TikTok Script Generator API",
    description="Standalone API to generate TikTok scripts using Apify and OpenAI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(tiktok_script.router, tags=["tiktok"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "TikTok Script Generator API", 
        "status": "running",
        "endpoints": {
            "tiktok_script": "/api/tiktok/script",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)