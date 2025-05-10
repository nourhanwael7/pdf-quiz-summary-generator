import requests
import json
import re
import logging
import time
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ollama API configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:latest"  

def call_ollama_api(prompt: str, max_retries: int = 3) -> Dict[str, Any]:
    """
    Call the Ollama API with retry logic
    
    Args:
        prompt: The text prompt to send to the model
        max_retries: Maximum number of retry attempts
        
    Returns:
        JSON response from Ollama API
        
    Raises:
        Exception: If all retry attempts fail
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.3,  # Slightly increased for better variety in questions
        "system": "You are a helpful assistant that creates high-quality educational content."
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Request failed (attempt {attempt+1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise

def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    Extract JSON from text that may contain additional formatting
    
    Args:
        text: Text that contains JSON data, possibly with markdown formatting
        
    Returns:
        Parsed JSON data as dictionary
    """
    logger.info(f"Trying to extract JSON from text: {text[:100]}...")

    json_match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1).strip()
    else:
        json_str = text.strip()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")

        try:
            # Try to fix common JSON formatting issues
            fixed_json = re.sub(r'(?<!\\)"(.*?)(?<!\\)"', r'"\1"', json_str)
            fixed_json = re.sub(r'}\s*{', '},{', fixed_json)
            if not fixed_json.strip().startswith('{'):
                fixed_json = '{' + fixed_json
            if not fixed_json.strip().endswith('}'):
                fixed_json = fixed_json + '}'

            return json.loads(fixed_json)
        except:
            logger.error("Failed to repair malformed JSON, creating a fallback structure")

            questions = []
            q_blocks = re.findall(
                r'question["\s:]+([^"]+)["\s,]+options["\s:]+\[(.*?)\]["\s,]+correctAnswer["\s:]+["]([^"]+)["\s,]+explanation["\s:]+["]([^"]+)',
                text,
                re.DOTALL
            )

            for q, opts, ans, exp in q_blocks:
                options = re.findall(r'"([^"]+)"', opts)
                if len(options) < 4:
                    options.extend(["Extra option"] * (4 - len(options)))

                questions.append({
                    "question": q.strip(),
                    "options": options[:4],
                    "correctAnswer": ans.strip(),
                    "explanation": exp.strip()
                })

            if not questions:
                raise ValueError("No questions found in the text")

            return {"questions": questions}
