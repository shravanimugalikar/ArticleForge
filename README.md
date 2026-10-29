# ✍️ ArticleForge

An autonomous multi-agent content creation studio powered by **CrewAI**, **Groq**, and **Gradio**. 

ArticleForge orchestrates a collaborative team of specialized AI agents—**Content Planner**, **Content Writer**, and **Editor**—to generate comprehensive, publication-ready articles from a single topic prompt.

---

## 🚀 Features

- **Autonomous Agent Crew**:
  - 📋 **Content Planner**: Researches trends, analyzes audience personas, identifies SEO keywords, and formulates a content outline.
  - ✍️ **Content Writer**: Drafts an insightful, engaging article following the planner's structured outline.
  - 🔍 **Editor**: Polishes grammar, verifies tone, ensures journalistic standards, and formats the output.
- **Ultra-Fast LLM Inference**: Powered by high-speed models via **Groq** (`openai/gpt-oss-120b`).
- **Interactive Web Interface**: Clean and intuitive **Gradio** UI with real-time progress tracking and one-click topic examples.

---

## 🛠️ Architecture

```mermaid
flowchart LR
    A["Topic Input"] --> B["Content Planner"]
    B -->|"Outline & SEO Keywords"| C["Content Writer"]
    C -->|"Draft Article"| D["Editor"]
    D --> E["Publication-Ready Article (Markdown)"]
```

---

## 📦 Project Structure

```text
ArticleForge/
│
├── article_forge.py       # Main application (CrewAI pipeline + Gradio UI)
├── requirements.txt       # Python dependencies
├── .env.example           # Template for environment variables
├── .gitignore             # Git ignore file for secrets and cache
└── README.md              # Project documentation
```

---

## ⚡ Quick Start

### 1. Prerequisites
- Python **3.10+** installed.
- A **Groq API Key** (obtain one for free at [Groq Console](https://console.groq.com/)).

### 2. Clone the Repository
```bash
git clone https://github.com/shravanimugalikar/ArticleForge.git
cd ArticleForge
```

### 3. Create a Virtual Environment (Optional but Recommended)
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure API Key
Create a `.env` file in the project root:
```bash
# Copy template
cp .env.example .env
```
Open `.env` and add your Groq API key:
```env
GROQ_API_KEY="your_groq_api_key_here"
```

### 6. Run the Application
```bash
python article_forge.py
```

The Gradio web interface will automatically launch in your browser at `http://127.0.0.1:7860`.

---

## Author

Shravani Mugalikar
