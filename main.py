import os
import string
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
SLUG_LENGTH = int(os.getenv("SLUG_LENGTH", 6))
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

app = FastAPI(
    title="URL Shortener API",
    description="Servicio básico para acortar URLs",
    version="0.1.0"
)

url_map: dict[str, str] = {}

class UrlCreate(BaseModel):
    url: str

class UrlResponse(BaseModel):
    slug: str
    shortened_url: str

@app.post("/shorten", response_model=UrlResponse)
def shorten_url(payload: UrlCreate):
    original_url = payload.url
    slug = ''.join(random.choices(string.ascii_letters + string.digits, k=SLUG_LENGTH))
    while slug in url_map:
        slug = ''.join(random.choices(string.ascii_letters + string.digits, k=SLUG_LENGTH))
    url_map[slug] = original_url
    return UrlResponse(slug=slug, shortened_url=f"{BASE_URL}/{slug}")

@app.get("/{slug}")
def redirect(slug: str):
    if slug in url_map:
        return {"url": url_map[slug]}
    raise HTTPException(status_code=404, detail="Slug not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
