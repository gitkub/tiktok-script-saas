from fastapi import APIRouter, HTTPException
from apify_client import ApifyClient
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ACTOR_ID = 'emQXBCL3xePZYgJyn'  # TikTok transcript extraction actor

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

@router.get("/api/tiktok/script")
async def generate_script_from_transcript(video_url: str):
    """Generate TikTok scripts from video transcript"""
    
    if not video_url:
        raise HTTPException(status_code=400, detail="Video URL is required")
    
    if not APIFY_TOKEN:
        raise HTTPException(status_code=500, detail="APIFY_TOKEN environment variable is required")
    
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable is required")
    
    try:
        # Get transcript from TikTok using Apify
        client = ApifyClient(APIFY_TOKEN)
        run_input = {"videos": [video_url]}
        run = client.actor(ACTOR_ID).call(run_input=run_input)

        transcript = ""
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            if "transcript" in item:
                transcript = item["transcript"]
                break
        
        if not transcript:
            raise HTTPException(status_code=404, detail="Transcript not found for this video")
        
        # Generate script using OpenAI
        prompt = f"""
จาก transcript นี้: "{transcript}"

โปรดวิเคราะห์และสรุปสไตล์การพูด เนื้อหา และโทนของต้นฉบับ จากนั้นสร้างสคริปต์ TikTok 4 แบบใหม่ในแนวเดียวกัน โดยใช้เนื้อหาจาก transcript ที่ให้มา

ข้อกำหนด:
- แต่ละสคริปต์ควรมีความยาวประมาณ 30-60 วินาที
- เหมาะสำหรับ TikTok และมี engagement สูง
- ใช้สไตล์การพูดและโทนเดียวกับต้นฉบับ

โปรดตอบกลับในรูปแบบ JSON ดังนี้:
{{
    "script_1": "สคริปต์ที่ 1",
    "script_2": "สคริปต์ที่ 2",
    "script_3": "สคริปต์ที่ 3",
    "script_4": "สคริปต์ที่ 4"
}}
"""

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "คุณเป็นผู้เชี่ยวชาญในการสร้างสคริปต์ TikTok ที่น่าสนใจและน่าเชื่อถือ"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        generated_script = response.choices[0].message.content
        
        return {
            "success": True,
            "original_transcript": transcript,
            "generated_scripts": generated_script,
            "video_url": video_url,
            "scripts_count": 4
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating script: {str(e)}")

@router.get("/")
async def tiktok_root():
    """TikTok script generator root endpoint"""
    return {"message": "TikTok Script Generator", "status": "running"}