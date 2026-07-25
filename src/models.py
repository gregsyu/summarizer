from pydantic import BaseModel, Field
from typing import Literal, Annotated

Styles = Literal["concise", "detailed", "bullet_points", "professional"]
Tones = Literal["professional", "casual", "funny", "persuasive", "educational"]
ContentTypes = Literal[
    "blog_post", "social_media", "email", "product_description", "youtube_script"
]


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description="Text to summarize")
    max_length: Annotated[
        int | None, Field(ge=50, le=1000, description="Max words in summary")
    ] = 200
    style: Styles = "concise"


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3, description="Main topic or title")
    content_type: ContentTypes = "blog_post"
    tone: Tones = "professional"
    length: Annotated[
        int | None, Field(ge=100, le=2000, description="Approximate word count")
    ] = 400
    extra_instructions: str | None = None


class ContentResponse(BaseModel):
    content: str
    word_count: int


class DocumentUploadRequest(BaseModel):
    max_length: Annotated[int | None, Field(ge=100, le=1500)] = 400
    style: Styles = "detailed"


class DocumentSummaryResponse(BaseModel):
    filename: str
    content: str
    word_count: int
    chunks_processed: int
    model_used: str
