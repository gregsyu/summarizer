# Summarizer

A FastAPI-based service for text summarization and content generation powered by Ollama and LangChain.

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
- Ollama running locally (default: `http://localhost:11434`)

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

```env
MODEL=ollama
BASE_URL=http://localhost:11434
ALLOW_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
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
