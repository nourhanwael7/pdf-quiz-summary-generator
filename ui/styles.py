import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to improve the UI appearance."""
    st.markdown("""
    <style>
    /* Main layout adjustments */
    .main .block-container {
        max-width: 70%;  /* Take more than half but not all of the page */
        padding-top: 2rem;
        padding-bottom: 2rem;
        margin: 0 auto;
    }
    
    /* Typography styling */
    h1, h2, h3 {
        color: #7E57C2;  /* Soft purple for headings */
        font-weight: 600;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    h2 {
        font-size: 2rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    h3 {
        font-size: 1.5rem;
        margin: 1.2rem 0 0.8rem 0;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 20px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button[data-baseweb="button"] {
        background-color: #9575CD;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* App header styling */
    .app-header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid #f0f0f0;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #9C27B0 0%, #673AB7 100%);
        color: white;
        border-radius: 10px;
    }
    
    .app-header h1 {
        color: white !important;
        margin: 0;
    }
    
    /* Form elements styling */
    div[data-baseweb="select"] {
        border-radius: 10px;
    }
    
    /* File uploader styling */
    .uploadedFile {
        border-radius: 10px !important;
        border: 2px dashed #9575CD !important;
        padding: 15px !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 5px 5px 0 0;
        padding: 0px 16px;
        font-weight: 500;
    }
    
    /* Alert message styling */
    .stAlert {
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 500;
        color: #5E35B1;
    }
    
    /* Divider styling */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #9575CD, transparent);
    }
    
    /* Quiz styling */
    .stRadio > div {
        flex-direction: row;
        gap: 1rem; 
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #9575CD !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #5E35B1;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1.2rem !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #F3E5F5;
    }
    
    /* Code block styling */
    .stCodeBlock {
        border-radius: 10px;
        background-color: #F5F5F5;
    }
    
    /* Container styling */
    [data-testid="stVerticalBlock"] > div:has(.stMarkdown h3) {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    /* Text colors for accessibility */
    p, li {
        color: #333333;
    }
    
    /* Custom animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .main .block-container {
        animation: fadeIn 0.5s ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)


def set_page_config():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Quiz & Summary Generator",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed"  # Hide sidebar by default
    )


def theme_color_palette():
    """Return a dictionary of theme colors for consistent styling."""
    return {
        "primary": "#9575CD",
        "secondary": "#5E35B1",
        "background": "#F3E5F5",
        "text": "#333333",
        "success": "#4CAF50",
        "warning": "#FFC107",
        "error": "#F44336",
        "info": "#2196F3"
    }


def apply_dark_mode():
    """Apply dark mode styling."""
    st.markdown("""
    <style>
    /* Dark mode overrides */
    body {
        color: #E0E0E0;
        background-color: #121212;
    }
    
    .main .block-container {
        background-color: #1E1E1E;
    }
    
    p, li, label, .stMarkdown {
        color: #E0E0E0 !important;
    }
    
    h1, h2, h3, h4, h5 {
        color: #BB86FC !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1E1E1E;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #BB86FC;
    }
    
    .stCodeBlock {
        background-color: #2D2D2D;
    }
    
    .stAlert {
        background-color: #2D2D2D;
    }
    
    [data-testid="stVerticalBlock"] > div:has(.stMarkdown h3) {
        background-color: #2D2D2D;
    }
    
    .app-header {
        background: linear-gradient(135deg, #7B1FA2 0%, #512DA8 100%);
    }
    
    .stButton>button[data-baseweb="button"] {
        background-color: #BB86FC;
        color: #000000;
    }
    
    /* Dark mode metrics */
    [data-testid="stMetricValue"] {
        color: #BB86FC !important;
    }
    </style>
    """, unsafe_allow_html=True)


def apply_responsive_design():
    """Apply additional CSS for responsive design on different screen sizes."""
    st.markdown("""
    <style>
    /* Mobile responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            max-width: 100%;
            padding: 1rem;
        }
        
        h1 {
            font-size: 1.8rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        h3 {
            font-size: 1.2rem;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        
        .stRadio > div {
            flex-direction: column;
        }
    }
    
    /* Tablet responsive design */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            max-width: 85%;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def apply_print_styles():
    """Apply styles specific for print layout."""
    st.markdown("""
    <style>
    @media print {
        .stButton, .stSidebar, .stTabs [data-baseweb="tab-list"] {
            display: none !important;
        }
        
        .main .block-container {
            max-width: 100%;
            padding: 0;
        }
        
        body {
            color: black;
            background-color: white;
        }
        
        p, li, h1, h2, h3, h4, h5 {
            color: black !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def apply_all_styles(include_dark_mode=False, include_responsive=True, include_print=True):
    """Apply all styles with optional configs."""
    set_page_config()
    apply_custom_styles()
    
    if include_responsive:
        apply_responsive_design()
    
    if include_dark_mode:
        apply_dark_mode()
    
    if include_print:
        apply_print_styles()
