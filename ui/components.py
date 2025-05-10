import streamlit as st
from typing import List, Dict, Any, Optional, Callable

def header():
    """Render the application header."""
    st.markdown("""
    <div class="app-header">
        <h1>📚 Quiz & Summary Generator</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Upload a PDF file and the system will help you:
    1. Generate a comprehensive summary of the document's content
    2. Create an interactive multiple-choice quiz based on its content
    
    Perfect for students, educators, and anyone looking to extract key information from documents!
    """)

def file_uploader() -> Optional[st.runtime.uploaded_file_manager.UploadedFile]:
    """Render the file uploader component."""
    st.markdown("### 📄 Upload Your Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF file", 
        type=["pdf"], 
        help="Upload any PDF document to generate a summary and quiz"
    )
    
    if uploaded_file:
        st.info("✅ File uploaded successfully! Let's begin processing.")
        
        with st.expander("Preview file details"):
            st.write(f"**File name:** {uploaded_file.name}")
            st.write(f"**File size:** {round(len(uploaded_file.getvalue())/1024, 2)} KB")
    
    return uploaded_file

def content_preview(content: str):
    """Render a preview of the extracted PDF content."""
    with st.expander("Preview extracted content"):
        st.text(content[:500] + "..." if len(content) > 500 else content)

def tabs_interface(
    summary_callback: Callable,
    quiz_callback: Callable,
    has_pdf_content: bool
):
    """Render the tabbed interface for summary and quiz."""
    tab1, tab2 = st.tabs([" Summary", " Quiz"])
    
    with tab1:
        st.header("Document Summary")
        
        if has_pdf_content:
            if st.button(" Generate Summary", key="gen_summary") or "summary_text" in st.session_state:
                summary_callback()
        else:
            st.warning("Please upload a PDF document first to generate a summary.")
    
    with tab2:
        st.header("Interactive Quiz")
        
        if has_pdf_content:
            if st.button(" Generate Quiz", key="gen_quiz") or "quiz_data" in st.session_state:
                quiz_callback()
                
            # Create new quiz button
            if "quiz_data" in st.session_state and st.session_state.quiz_data:
                if st.button("🔄 Create New Quiz", key="new_quiz"):
                    # Clear previous quiz data to force regeneration
                    st.session_state.quiz_data = None
                    st.session_state.quiz_submitted = False
                    st.session_state.user_answers = []
                    st.session_state.score = 0
                    
                    # Regenerate quiz
                    with st.spinner("Generating new quiz questions..."):
                        quiz_callback(force_new=True)
        else:
            st.warning("Please upload a PDF document first to generate a quiz.")

def display_summary(summary_text: str):
    """Display the PDF summary on the Streamlit interface."""
    st.subheader("Document Summary")
    st.markdown(summary_text)
    
    # Add a copy to clipboard button
    if st.button("Copy Summary to Clipboard"):
        st.code(summary_text)
        st.success("Summary copied to clipboard! (Use Ctrl+C to copy the text above)")

def display_interactive_quiz(quiz_data: Dict[str, Any]):
    """Display the interactive quiz on the Streamlit interface."""
    if "error" in quiz_data:
        st.error(quiz_data["error"])
        return

    questions = quiz_data.get("questions", [])
    if not questions:
        st.warning("No questions generated. The document may lack sufficient content.")
        return

    st.success(f"{len(questions)} questions generated successfully!")
    
    # Initialize user's answers in session state if not already present
    # OR if the length doesn't match the number of questions
    if "user_answers" not in st.session_state or len(st.session_state.user_answers) != len(questions):
        st.session_state.user_answers = [""] * len(questions)
    
    # Initialize quiz submission state
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    
    # Initialize score tracking
    if "score" not in st.session_state:
        st.session_state.score = 0

    # Function to handle the submit button click
    def submit_quiz():
        st.session_state.quiz_submitted = True
        # Calculate score
        correct_count = 0
        for i, q in enumerate(questions):
            if st.session_state.user_answers[i] == q["correctAnswer"]:
                correct_count += 1
        st.session_state.score = correct_count

    # Display all questions
    for i, q in enumerate(questions):
        question_container = st.container()
        with question_container:
            st.subheader(f"Question {i+1}")
            st.write(q["question"])

            # Create radio buttons for each question
            try:
                # Only try to get index if the user has actually selected something
                if st.session_state.user_answers[i] and st.session_state.user_answers[i] in q["options"]:
                    index = q["options"].index(st.session_state.user_answers[i])
                else:
                    index = None
                    
                option_selected = st.radio(
                    f"Select your answer for question {i+1}:",
                    q["options"],
                    key=f"q_{i}",
                    index=index,
                    disabled=st.session_state.quiz_submitted,
                    horizontal=True
                )
            except (ValueError, IndexError):
                # Fallback in case of any error
                option_selected = st.radio(
                    f"Select your answer for question {i+1}:",
                    q["options"],
                    key=f"q_{i}",
                    index=None,
                    disabled=st.session_state.quiz_submitted,
                    horizontal=True
                )
            
            # Store user's selection in session state
            st.session_state.user_answers[i] = option_selected
            
            # If the quiz has been submitted, show if the answer was correct and the explanation
            if st.session_state.quiz_submitted:
                is_correct = option_selected == q["correctAnswer"]
                if is_correct:
                    st.success("✓ Correct!")
                else:
                    st.error(f"✗ Incorrect. The correct answer is: {q['correctAnswer']}")
                
                st.info(f"Explanation: {q['explanation']}")
            
            st.divider()

    # Submit button
    if not st.session_state.quiz_submitted:
        st.button("Submit Quiz", on_click=submit_quiz, type="primary")
    else:
        # Display final score
        score_percentage = (st.session_state.score / len(questions)) * 100
        st.metric(
            label="Your Score", 
            value=f"{st.session_state.score}/{len(questions)}", 
            delta=f"{score_percentage:.1f}%"
        )
        
        # Feedback based on score
        if score_percentage >= 80:
            st.success("🎉 Excellent! You've mastered this content.")
        elif score_percentage >= 60:
            st.info("👍 Good job! You understand most of the material.")
        else:
            st.warning("📚 Keep studying! You might want to review the summary again.")
        
        # Restart button
        if st.button("Restart Quiz"):
            st.session_state.quiz_submitted = False
            st.session_state.user_answers = [""] * len(questions)
            st.session_state.score = 0
            st.rerun()

def display_error(message: str):
    """Display an error message with styling."""
    st.error(message)
    
def display_loading(message: str = "Processing..."):
    """Display a loading spinner with a custom message."""
    return st.spinner(message)

def display_ollama_status(is_connected: bool, model_name: str, available_models: List[str] = None):
    """Display Ollama connection status."""
    if is_connected:
        if model_name in (available_models or []):
            st.sidebar.success(f"✅ Connected to Ollama with model: {model_name}")
        else:
            st.sidebar.warning(f"⚠️ Ollama is running, but model '{model_name}' is not available.")
            st.sidebar.info(f"Pull it using: `ollama pull {model_name}`")
    else:
        st.sidebar.error("❌ Cannot connect to Ollama API. Make sure it's running on port 11434.")
