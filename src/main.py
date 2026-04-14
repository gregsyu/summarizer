from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from .models import ContentResponse, GenerateRequest, SummarizeRequest
from .prompts import summarize_prompt, generate_prompt

load_dotenv()

app = FastAPI(
    title="Summarizer",
    description="Simple summarizer and content generator",
    version="0.1.0",
)

llm = ChatOllama(model=os.getenv("MODEL"), base_url=os.getenv("BASE_URL"))

summarize_chain = summarize_prompt | llm | StrOutputParser()
generate_chain = generate_prompt | llm | StrOutputParser()

# Endpoints:


@app.post("/summarize", response_model=ContentResponse)
async def summarize(request: SummarizeRequest):
    try:
        result = summarize_chain.invoke(
            {
                "text": request.text,
                "max_length": request.max_length,
                "style": request.style.replace("_", " "),
            }
        )

        return ContentResponse(content=result.strip(), word_count=len(result.split()))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating summary: {str(e)}"
        )


@app.post("/generate", response_model=ContentResponse)
async def generate_content(request: GenerateRequest):
    try:
        # Assigns the value on the right if the left side is None
        extra = request.extra_instructions or "Focus on value"

        result = generate_chain.invoke(
            {
                "topic": request.topic,
                "content_type": request.content_type.replace("_", " "),
                "tone": request.tone,
                "length": request.length,
                "extra_instructions": extra,
            }
        )

        return ContentResponse(content=result.strip(), word_count=len(result.split()))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating content: {str(e)}"
        )


@app.get("/")
async def root():
    return {
        "message": "Summarizer is running!",
        "endpoints": ["/summarize", "/generate"],
        "docs": "/docs",
    }
