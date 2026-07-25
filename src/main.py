from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    ContentResponse,
    GenerateRequest,
    SummarizeRequest,
    DocumentSummaryResponse,
    DocumentUploadRequest,
)
from .settings import settings
from .prompts import summarize_prompt, generate_prompt, document_summary_prompt
from .document_processor import process_uploaded_file
from typing import Annotated
from pydantic import SecretStr

app = FastAPI(
    title="Summarizer",
    description="Simple summarizer and content generator",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_llm():
    provider = settings.LLM_PROVIDER.lower()
    api_key = SecretStr(settings.API_KEY)

    match provider:
        case "ollama":
            return ChatOllama(model=settings.MODEL, base_url=settings.BASE_URL)
        case "groq":
            return ChatGroq(model=settings.MODEL, api_key=api_key)
        case "openai":
            return ChatOpenAI(model=settings.MODEL, api_key=api_key)
        case "anthropic":
            return ChatAnthropic(
                model_name=settings.MODEL, api_key=api_key
                )
        case _:
            raise ValueError(
                f"Unsupported LLM provider: {provider}. " +
                "Supported providers: ollama, groq, openai, anthropic"
            )


llm = get_llm()

summarize_chain = summarize_prompt | llm | StrOutputParser()
generate_chain = generate_prompt | llm | StrOutputParser()
document_summary_chain = document_summary_prompt | llm | StrOutputParser()

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

        return ContentResponse(
            content=result.strip(), word_count=len(result.split())
            )
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

        return ContentResponse(
            content=result.strip(), word_count=len(result.split())
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating content: {str(e)}"
        )


@app.post("/upload-and-summarize", response_model=DocumentSummaryResponse)
async def upload_and_summarize(
    file: Annotated[UploadFile, File(...)],
    # `Depends()` make it use it as query parameters
    request: Annotated[DocumentUploadRequest, Depends()],
):
    try:
        split_docs = await process_uploaded_file(file)
        full_text = "\n\n".join([doc.page_content for doc in split_docs])
        result = document_summary_chain.invoke(
            {
                "text": full_text,
                "max_length": request.max_length,
                "style": request.style.replace("_", " "),
            }
        )

        if file.filename is None:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file must have a filename",
            )

        response = DocumentSummaryResponse(
            filename=file.filename,
            content=result.strip(),
            word_count=len(result.split()),
            chunks_processed=len(split_docs),
            model_used=settings.MODEL,
        )
        return response
    except HTTPException:
        raise
    except Exception as e:  # it catches all exceptions
        raise HTTPException(
            status_code=500, detail=f"Failed to process document: {str(e)}"
        )


@app.get("/")
async def root():
    return {
        "message": "Summarizer is running!",
        "endpoints": ["/summarize", "/generate", "/upload-and-summarize"],
        "docs": "/docs",
    }
