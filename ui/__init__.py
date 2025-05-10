"""
UI package for the PDF Quiz & Summary Generator application.

This package contains components and styles for the Streamlit-based user interface.
"""

from src.ui.components import (
    header,
    file_uploader,
    content_preview,
    tabs_interface,
    display_summary,
    display_interactive_quiz,
    display_error,
    display_loading,
    display_ollama_status
)

from src.ui.styles import (
    apply_all_styles,
    theme_color_palette,
    apply_custom_styles,
    apply_dark_mode,
    apply_responsive_design,
    apply_print_styles,
    set_page_config
)

__all__ = [
    # Components
    'header',
    'file_uploader',
    'content_preview',
    'tabs_interface',
    'display_summary',
    'display_interactive_quiz',
    'display_error',
    'display_loading',
    'display_ollama_status',
    
    # Styles
    'apply_all_styles',
    'theme_color_palette',
    'apply_custom_styles',
    'apply_dark_mode',
    'apply_responsive_design',
    'apply_print_styles',
    'set_page_config'
]
