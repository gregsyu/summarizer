
from pydantic import BaseModel, Field
from typing import Optional, Literal

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description="Text to summarize")
    max_length: Optional[int] = Field(200, ge=50, le=1000, description="Max words in summary")
    style: Literal["concise", "detailed", "bullet_points", "professional"] = "concise"

class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3, description="Main topic or title")
    content_type: Literal["blog_post", "social_media", "email", "product_description", "youtube_script"] = "blog_post"
    tone: Literal["professional", "casual", "funny", "persuasive", "educational"] = "professional"
    length: Optional[int] = Field(400, ge=100, le=2000, description="Approximate word count")
    extra_instructions: Optional[str] = None

class ContentResponse(BaseModel):
    content: str
    word_count: int