# PDF Quiz & Summary Generator

A Streamlit application that uses Local Language Models (via Ollama) to generate comprehensive summaries and interactive quizzes from PDF documents.

![PDF Quiz & Summary Generator](https://i.postimg.cc/BZK8D1H1/Chat-GPT-Image-May-10-2025-01-26-21-AM.png)

## 🌟 Features

- 📄 **PDF Text Extraction**: Efficiently extracts text content from uploaded PDF documents
- 📝 **AI-Powered Summarization**: Generates detailed summaries that capture the essence of documents
- ❓ **Interactive Quizzes**: Creates dynamic multiple-choice quizzes with automatic scoring
- 🎨 **Clean, Responsive UI**: Beautiful Streamlit interface with custom styling
- 🤖 **Offline LLM Support**: Uses Ollama to run language models locally

## 📋 Requirements

- Python 3.8+
- Ollama with the llama3:latest model (or modify the code to use your preferred model)
- Required Python packages (see requirements.txt)

## 🚀 Quick Start

**Clone the Repository:**
```bash
git clone https://github.com/nourhanwael7/pdf-quiz-summary-generator.git
cd pdf-quiz-summary-generator
```

**Create a Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Install Ollama:**
- Follow instructions at [ollama.ai](https://ollama.ai)

**Pull the Required Model:**
```bash
ollama pull llama3:latest
```

**Run the Application:**
```bash
streamlit run app.py
```

**Open in Browser:**
- Navigate to http://localhost:8501

## 💻 Usage

1. Upload a PDF document
2. Select either the Summary or Quiz tab
3. Click the "Generate Summary" or "Generate Quiz" button
4. View the generated content or take the interactive quiz
5. Copy summaries to clipboard or submit quizzes to see your score



