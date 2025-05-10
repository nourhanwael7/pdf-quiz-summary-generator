import PyPDF2
import logging
import tempfile
from typing import Optional, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(uploaded_file) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract text from PDF file
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Tuple containing:
            - PDF content as string (or None if failed)
            - Error message (or None if successful)
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file.flush()

            pdf_reader = PyPDF2.PdfReader(tmp_file.name)
            pdf_content = ""
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    pdf_content += text + "\n"

            if not pdf_content.strip():
                return None, "No readable content found in the PDF. Please upload a valid document."

            return pdf_content, None
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        return None, f"Error processing PDF: {str(e)}"
