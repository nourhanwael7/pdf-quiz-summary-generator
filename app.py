import streamlit as st
import logging
from src.pdf_processor import extract_text_from_pdf
from src.summary_generator import generate_summary
from src.quiz_generator import generate_quiz
from src.ui_components import display_interactive_quiz, display_summary
from assets.styles import apply_custom_css
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ollama model configuration
MODEL_NAME = "llama3:latest"

def main():
    """Main Streamlit app function"""
    # Set wider page layout
    st.set_page_config(
        page_title="Quiz & Summary Generator",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed"  # Hide sidebar by default
    )
    
    # Apply custom CSS for better styling
    apply_custom_css()
    
    # Title 
    st.title("📚 Quiz & Summary Generator")
    
    st.markdown("""
    Upload a PDF file and the system will help you:
    1. Generate a comprehensive summary of the document's content
    2. Create an interactive multiple-choice quiz based on its content
    
    Perfect for students, educators, and anyone looking to extract key information from documents!
    """)
    
    # Check Ollama availability
    try:
        response = requests.get("http://localhost:11434/api/tags")  
        models = [model["name"] for model in response.json()["models"]]
        if MODEL_NAME not in models:
            st.warning(f"Model '{MODEL_NAME}' is not available in Ollama. Pull it using: `ollama pull {MODEL_NAME}`")
    except requests.RequestException:
        st.error("Cannot connect to Ollama API. Make sure it's running on port 11434.")

    # File upload section with improved UI
    st.markdown("### 📄 Upload Your Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], 
                                      help="Upload any PDF document to generate a summary and quiz")

    if uploaded_file:
        st.info("✅ File uploaded successfully! Let's begin processing.")

        # Store processed data in session state to preserve it between reruns
        if "quiz_data" not in st.session_state:
            st.session_state.quiz_data = None
            
        if "summary_text" not in st.session_state:
            st.session_state.summary_text = None

        # Process PDF and extract content
        if "pdf_content" not in st.session_state:
            with st.spinner("Reading document content... This may take a moment."):
                pdf_content, error = extract_text_from_pdf(uploaded_file)
                if error:
                    st.error(error)
                elif pdf_content:
                    st.session_state.pdf_content = pdf_content
                    with st.expander("Preview extracted content"):
                        st.text(pdf_content[:500] + "...")
        
        # Create tabs for different functionalities with nicer styling
        tab1, tab2 = st.tabs([" Summary", " Quiz"]) 
        
        with tab1:
            st.header("Document Summary")
            
            # Generate Summary button
            if st.button(" Generate Summary", key="gen_summary") or st.session_state.summary_text: 
                # Only process if we don't already have summary data
                if not st.session_state.summary_text:
                    with st.spinner("Generating comprehensive document summary... This may take a few minutes."):
                        summary = generate_summary(st.session_state.pdf_content)
                        st.session_state.summary_text = summary
                
                # Display the summary
                display_summary(st.session_state.summary_text)

        with tab2:
            st.header("Interactive Quiz")
            
            # Generate Quiz button
            if st.button(" Generate Quiz", key="gen_quiz") or st.session_state.quiz_data: 
                # Only process if we don't already have quiz data
                if not st.session_state.quiz_data:
                    with st.spinner("Creating quiz questions... This may take a few minutes."):
                        st.session_state.quiz_data = generate_quiz(st.session_state.pdf_content)
                        
                        # Reset user answers for the new quiz
                        questions = st.session_state.quiz_data.get("questions", [])
                        st.session_state.user_answers = [""] * len(questions)
                        st.session_state.quiz_submitted = False
                        st.session_state.score = 0
                
                # Always display the quiz if we have data
                display_interactive_quiz(st.session_state.quiz_data)
                
            # Create new quiz button
            if "quiz_data" in st.session_state and st.session_state.quiz_data:
                if st.button("🔄 Create New Quiz", key="new_quiz"):
                    # Clear previous quiz data to force regeneration
                    st.session_state.quiz_data = None
                    st.session_state.quiz_submitted = False
                    st.session_state.user_answers = []  # Reset to empty list first
                    st.session_state.score = 0
                    
                    # Regenerate quiz
                    with st.spinner("Generating new quiz questions..."):
                        st.session_state.quiz_data = generate_quiz(st.session_state.pdf_content)
                        
                        # Initialize user_answers with correct length for new quiz
                        questions = st.session_state.quiz_data.get("questions", [])
                        st.session_state.user_answers = [""] * len(questions)
                        
                        st.rerun()
        
if __name__ == "__main__":
    main()
