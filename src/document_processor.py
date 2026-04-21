import tempfile
import os
from functools import partial
from fastapi import UploadFile, HTTPException
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Dict, Callable

SUPPORTED_EXTENSIONS: Dict[str, Callable] = {
    ".pdf": PyPDFLoader,
    ".txt": partial(TextLoader, encoding="utf-8"),
    ".docx": Docx2txtLoader,
    ".md": UnstructuredMarkdownLoader,
}


async def process_uploaded_file(file: UploadFile) -> List[Document]:
    file_ext = os.path.splitext(file.filename.lower())[1]

    if file_ext not in SUPPORTED_EXTENSIONS.keys():
        supported = ", ".join(SUPPORTED_EXTENSIONS.keys())
        raise HTTPException(
            status_code=400, detail=f"Only {supported} files are supported."
        )

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=400, detail="File too large. Maximum size is 10MB."
        )

    # recommended way to pass a file path to loaders that will open the file themselves:
    # with/try/finally
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
        tmp_file.write(content)
        tmp_path = tmp_file.name
        # close temporary file here

    try:
        loader = SUPPORTED_EXTENSIONS[file_ext](tmp_path)

        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500, chunk_overlap=150, length_function=len
        )
        split_docs = text_splitter.split_documents(documents)

        for doc in split_docs:
            doc.metadata["source"] = file.filename
            doc.metadata["file_type"] = file_ext[1:].upper()
        return split_docs
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
