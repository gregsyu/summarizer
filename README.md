# Summarizer

A FastAPI-based service for text summarization and content generation powered by multiple LLM providers (Ollama, Groq, OpenAI, Anthropic) and LangChain.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check and available endpoints |
| `/summarize` | POST | Summarize provided text |
| `/generate` | POST | Generate content from a topic |
| `/upload-and-summarize` | POST | Upload a document and get a summary |
| `/docs` | GET | Interactive API documentation (Swagger UI) |

## Requirements

- Python 3.9+
- Ollama running locally (default: `http://localhost:11434`) OR API keys for cloud providers (Groq, OpenAI, Anthropic)

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Start Ollama with your preferred model
ollama serve

# Run the server
uvicorn src.main:app --reload
```

## Configuration

Set environment variables or use a `.env` file:

### Ollama (default)

```env
LLM_PROVIDER=ollama
MODEL=llama3.2
BASE_URL=http://localhost:11434
ALLOW_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### Groq

```env
LLM_PROVIDER=groq
MODEL=llama-3.3-70b-versatile
API_KEY=your_groq_api_key
```

### OpenAI

```env
LLM_PROVIDER=openai
MODEL=gpt-4o-mini
API_KEY=your_openai_api_key
```

### Anthropic

```env
LLM_PROVIDER=anthropic
MODEL=claude-sonnet-4-20250514
API_KEY=your_anthropic_api_key
```

## Example Usage

### Summarize Text

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Your long text here...", "max_length": 100, "style": "concise"}'
```

### Generate Content

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI safety", "content_type": "blog_post", "tone": "informative", "length": 500}'
```

### Upload and Summarize Document

```bash
curl -X POST http://localhost:8000/upload-and-summarize?max_length=150\&style=bullet_points \
  -F "file=@document.pdf"
```
