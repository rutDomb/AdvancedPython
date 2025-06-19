# 🔍 Code Analyzer FastAPI

A FastAPI-based system for static code analysis of various programming languages (Python, JavaScript, TypeScript, Java, etc.), providing both textual and graphical warnings about common issues in code.

---

## 🚀 Overview

This project offers real-time static analysis of uploaded code files, checking for:

- Overly long functions
- Files with too many lines
- Unused variables
- Missing function docstrings

Additionally, it generates charts and visualizations such as:

- Function length histograms
- Pie charts of issue types
- Bar charts comparing issues across files

---

## ⚙️ Installation & Usage

1. **Clone the project**:
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn matplotlib
   ```

4. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API documentation**:
   Open your browser and navigate to:
   ```
   http://localhost:8000/docs
   ```

---

## 📁 Project Structure

```
project/
│
├── main.py              # Main FastAPI file defining /alerts and /analyze endpoints
├── analyze.py           # Chart generation and function length extraction
├── alerts.py            # Code issue checks (function length, unused variables, etc.)
├── graphs/              # Folder to store generated PNG charts
│   └── *.png
├── README.md            # This documentation file
└── requirements.txt     # Project dependencies (optional)
```

---

## 🔌 API Endpoints

### 📍 POST `/alerts`

Performs textual analysis and returns warnings for each uploaded file.

**Input**:
- List of files (`multipart/form-data`)

**Example output**:
```json
[
  {
    "filename": "example.py",
    "warnings": [
      "Function 'foo' is too long: 31 lines",
      "Variable 'x' is assigned but never used"
    ]
  },
  {
    "filename": "broken.py",
    "error": "unexpected indent"
  }
]
```

---

### 📍 POST `/analyze`

Performs graphical analysis and returns:
- Function length histogram
- Pie chart of issue types
- Bar chart of total issues per file

**Input**:
- List of files (`multipart/form-data`)

**Example output**:
```json
{
  "files": [
    {
      "filename": "script.py",
      "function_length_graph": "/graphs/abcd1234.png",
      "issues_pie_chart": "/graphs/efgh5678.png"
    }
  ],
  "issues_bar_chart": "/graphs/ijkl9012.png"
}
```

---

## 🛠 Requirements

You can list the project dependencies in a `requirements.txt` file:

```txt
fastapi
uvicorn
matplotlib
```

To install them:
```bash
pip install -r requirements.txt
```

---

## 📝 Notes

- No database is used — data is processed in-memory and charts are saved as PNG files in the `graphs` directory.
- Supported file extensions: `.py`, `.java`, `.js`, `.ts`, `.cpp`, `.c`
- The current code mainly analyzes **Python** code, but includes basic keyword checks for other languages.
- Each chart is saved as a unique PNG file and accessible via `/graphs/<filename>`.

---

## 📧 Contact

For questions or issues, please contact the project maintainer.

---

Good luck! 🚀