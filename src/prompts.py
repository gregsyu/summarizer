from langchain_core.prompts import ChatPromptTemplate

summarize_prompt = ChatPromptTemplate.from_template(
    """You are an expert summarizer.
    Summarize the following text in a {style} way.
    Maximum length: around {max_length} words.

    Text:
    {text}

    Summary:"""
)

generate_prompt = ChatPromptTemplate.from_template(
    """You are a skilled content writer.
    Write a {content_type} about "{topic}".
    Tone: {tone}
    Approximate length: {length} words.

    {extra_instructions}

    Make it engaging, clear, and well-structured.
    Do not add any meta comments or explanations.

    Content:"""
)
