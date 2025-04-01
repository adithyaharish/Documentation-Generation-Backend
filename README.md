**Overview**
This project is a Documentation Generator that uses AI to create dynamic, interactive documentation from GitHub repositories. It allows users to generate documentation for various programming languages (e.g., Java, Python, JavaScript) and refine it using a conversation with AI. The tool supports multiple user levels (Beginner, Intermediate, Expert) and branch-wise documentation generation.

# 🧠 AutoDocGen – Intelligent Code Documentation Generator

This project automatically generates **clean, high-level documentation** from any public GitHub repository using Tree-sitter parsing, file grouping, and GPT-based summarization.

---

## 🔧 Features
- ✅ Supports multiple languages: **Python, JavaScript, Java, C++**
- 🧠 Uses **Tree-sitter** to parse structure (functions, classes, args)
- 🗂 Groups files by **import relationships, folder hierarchy, and naming**
- 🔍 Filters out **non-application/system files** with both logic + GPT
- 📄 LLM generates:
  - Full documentation (per file/group)
  - 1-line summary of each file
- 🌿 Handles **multiple branches**
- 🔌 Exposed as a **Flask API** for frontend usage

---

## 📁 Code Structure

| File / Folder | Description |
|---------------|-------------|
| `app.py` | Flask backend server – defines the `/default-doc` endpoint |
| `run_docgen_cli.py` | Main controller that runs the full doc generation logic |
| `docgen_from_github.py` | Clones repo, detects branches and language |
| `parse_all.py` | Parses all files using Tree-sitter and per-language logic |
| `group_chunks.py` | Groups files into chunks using imports + structure |
| `build_dependency_graph.py` | Builds a dependency graph of file imports |
| `summarizers/` | Summarizes code: GPT + heuristic logic |
| `utils/` | File filters, tree-sitter loader, helpers |
| `build/my-languages.so` | Precompiled Tree-sitter shared lib (needed for parsing) |

---

## 🚀 How to Run

### 1. 🔧 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 🔑 Set Your OpenAI API Key

Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. ▶️ Start the Flask Server

```bash
python app.py
```

### 4. 📡 API Usage

POST /default-doc 

```bash
{
  "repo_url": "https://github.com/username/repo",
  "branch": "main"
}
```
