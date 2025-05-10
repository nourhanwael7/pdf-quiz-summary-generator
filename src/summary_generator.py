import logging
from .llm_interface import call_ollama_api

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_summary_prompt(pdf_content: str) -> str:
    """
    Create the prompt to generate the summary
    
    Args:
        pdf_content: Text extracted from PDF
        
    Returns:
        Formatted prompt for the LLM
    """
    prompt = f"""
    Task: You are an expert educational content summarizer. Analyze the following PDF content and generate a comprehensive summary.

    PDF Content:
    ```
    {pdf_content[:5000]}
    ```

    Summary Requirements:
    1. Provide a detailed and comprehensive summary of the content
    2. Maintain all important points and key ideas
    3. Include main arguments, critical details, and major concepts
    4. Make the summary clear, coherent, and informative
    5. Structure the summary with logical flow using paragraphs and bullet points when appropriate
    6. The summary should allow someone to understand the essence of the document without reading it in full

    Your summary should be thorough yet concise, capturing the document's core message and important details.
    """
    return prompt

def generate_summary(pdf_content: str) -> str:
    """
    Generate a summary from PDF content
    
    Args:
        pdf_content: Text extracted from PDF
        
    Returns:
        Generated summary text
    """
    try:
        prompt = generate_summary_prompt(pdf_content)
        response = call_ollama_api(prompt)

        if 'response' not in response:
            return "Error: Invalid response from language model"

        return response['response']
    except Exception as e:
        logger.error(f"Summary generation error: {str(e)}")
        return f"Failed to generate summary: {str(e)}"
