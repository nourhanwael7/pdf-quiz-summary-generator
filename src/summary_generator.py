import logging
from .llm_interface import call_ollama_api

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_summary_prompt(pdf_content: str) -> str:
    """
    Create a prompt to generate a comprehensive and detailed summary of a document.
    The summary will include extensive details with each point on a separate line,
    read the entire file, and ensure no important information is skipped.
    """
    # Process the full content without any truncation
    full_content = pdf_content
    
    prompt = f"""
You are an expert document analyst tasked with creating a comprehensive and detailed summary. 
Analyze the ENTIRE document thoroughly without skipping any sections or important information.

DOCUMENT CONTENT:
```
{full_content}
```

SUMMARY INSTRUCTIONS:
1. Create an EXTREMELY DETAILED summary that captures ALL key information
2. Present each point on its own line for maximum clarity and readability
3. Ensure the summary is comprehensive, covering ALL sections of the document
4. Do not skip ANY important information, no matter how minor it may seem
5. Organize the information in a logical, structured format


Your summary must be so detailed and comprehensive that someone could understand 
the COMPLETE content of the document without reading the original. Leave nothing important out.
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
