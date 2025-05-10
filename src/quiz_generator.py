import logging
from typing import Dict, Any
from .llm_interface import call_ollama_api, extract_json_from_text

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_quiz_prompt(pdf_content: str) -> str:
    """
    Create the prompt to generate the quiz
    
    Args:
        pdf_content: Text extracted from PDF
        
    Returns:
        Formatted prompt for the LLM
    """
    prompt = f"""
    Task: You are an expert educational quiz creator. Analyze the following PDF content and generate a multiple-choice quiz.

    PDF Content:
    ```
    {pdf_content[:3000]}
    ```

    Quiz Requirements:
    1. Create 10 questions (or fewer if content is limited).
    2. Each question MUST include:
       - A clear and direct question
       - EXACTLY four answer options (A, B, C, D)
       - One correct answer
       - A brief explanation of the correct answer
    3. Ensure that all questions have exactly 4 options, not more, not less.

    Return the result in strict JSON format as follows:

    ```json
    {{
      "questions": [
        {{
          "question": "First question text",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "correctAnswer": "The correct option exactly as written",
          "explanation": "Explanation for the correct answer"
        }},
        {{
          "question": "Second question text",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "correctAnswer": "The correct option",
          "explanation": "Explanation for the correct answer"
        }}
      ]
    }}
    ```

    Start your response directly with ```json and end with ``` — any extra formatting outside of these tags will cause processing errors.
    """
    return prompt

def ensure_four_options(quiz_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure each question has exactly 4 options
    
    Args:
        quiz_data: Quiz data dictionary
        
    Returns:
        Processed quiz data with exactly 4 options per question
    """
    for question in quiz_data.get("questions", []):
        options = question.get("options", [])
        
        # If less than 4 options, add generic ones
        while len(options) < 4:
            options.append(f"Additional option {len(options) + 1}")
            
        # If more than 4 options, truncate
        if len(options) > 4:
            options = options[:4]
            
            # Make sure the correct answer is still in the options
            if question["correctAnswer"] not in options:
                options[3] = question["correctAnswer"]
                
        question["options"] = options
        
        # Ensure correctAnswer is in options
        if question["correctAnswer"] not in options:
            for opt in options:
                if question["correctAnswer"].lower() in opt.lower() or opt.lower() in question["correctAnswer"].lower():
                    question["correctAnswer"] = opt
                    break
            else:
                question["correctAnswer"] = options[0]
                
    return quiz_data

def generate_quiz(pdf_content: str) -> Dict[str, Any]:
    """
    Generate a quiz from PDF content
    
    Args:
        pdf_content: Text extracted from PDF
        
    Returns:
        Dictionary containing quiz data (questions, options, answers)
    """
    try:
        prompt = generate_quiz_prompt(pdf_content)
        response = call_ollama_api(prompt)

        if 'response' not in response:
            return {"error": "Invalid response from language model"}

        quiz_data = extract_json_from_text(response['response'])

        if "questions" not in quiz_data or not isinstance(quiz_data["questions"], list):
            return {"error": "Invalid quiz format, questions list not found"}

        # Ensure each question has exactly 4 options
        quiz_data = ensure_four_options(quiz_data)

        cleaned_questions = []
        for q in quiz_data["questions"]:
            if not all(key in q for key in ["question", "options", "correctAnswer", "explanation"]):
                continue

            if len(q["options"]) != 4:
                continue  # Skip questions that don't have exactly 4 options

            if q["correctAnswer"] not in q["options"]:
                for opt in q["options"]:
                    if q["correctAnswer"].lower() in opt.lower() or opt.lower() in q["correctAnswer"].lower():
                        q["correctAnswer"] = opt
                        break
                else:
                    q["correctAnswer"] = q["options"][0]

            cleaned_questions.append(q)

        if not cleaned_questions:
            return {"error": "No valid questions generated"}

        return {"questions": cleaned_questions}
    except Exception as e:
        logger.error(f"Quiz generation error: {str(e)}")
        return {"error": f"Failed to generate quiz: {str(e)}"}
