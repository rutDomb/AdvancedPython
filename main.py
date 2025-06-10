from fastapi import FastAPI, File, UploadFile, HTTPException
from alerts import (
    router as posts_router,
    check_function_length,
    check_file_length,
    check_unused_variables,
    check_missing_docstrings
)
import uvicorn
import ast
import os
from analyze import (
    extract_function_lengths,
    create_histogram,
    create_pie_chart,
    create_bar_chart
)
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/graphs", StaticFiles(directory="graphs"), name="graphs")

ALLOWED_EXTENSIONS = {'.py', '.java', '.js', '.ts', '.cpp', '.c'}

def is_code_file(filename: str, content: str) -> bool:
    _, ext = os.path.splitext(filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return False
    keywords = ['def ', 'function ', 'class ', 'import ', 'public ', 'const ', 'let ', '#include']
    return any(keyword in content for keyword in keywords)

@app.post("/alerts")
async def alerts(files: list[UploadFile] = File(...)):
    all_warnings = []

    for file in files:
        try:
            code_bytes = await file.read()
            code_text = code_bytes.decode("utf-8", errors="ignore")

            if not is_code_file(file.filename, code_text):
                raise HTTPException(status_code=400, detail=f"'{file.filename}' is not a recognized code file.")

            tree = ast.parse(code_text)
            warnings = []
            warnings += check_function_length(tree)
            warnings += check_file_length(code_text)
            warnings += check_unused_variables(tree)
            warnings += check_missing_docstrings(tree)

            all_warnings.append({
                "filename": file.filename,
                "warnings": warnings
            })
        except HTTPException as e:
            raise e
        except Exception as e:
            all_warnings.append({
                "filename": file.filename,
                "error": str(e)
            })

    return all_warnings

@app.post("/analyze")
async def analyze_code(files: list[UploadFile] = File(...)):
    results = []
    issues_per_file = {}

    for file in files:
        try:
            content = await file.read()
            code_text = content.decode("utf-8", errors="ignore")

            if not is_code_file(file.filename, code_text):
                raise HTTPException(status_code=400, detail=f"'{file.filename}' is not a recognized code file.")

            function_lengths = extract_function_lengths(code_text)
            graph_filename = create_histogram(function_lengths)
            tree = ast.parse(code_text)

            function_warnings = check_function_length(tree)
            file_warnings = check_file_length(code_text)
            unused_var_warnings = check_unused_variables(tree)
            docstring_warnings = check_missing_docstrings(tree)

            total_issues = (
                len(function_warnings) +
                len(file_warnings) +
                len(unused_var_warnings) +
                len(docstring_warnings)
            )
            issues_per_file[file.filename] = total_issues

            pie_filename = create_pie_chart({
                "Long functions": len(function_warnings),
                "Long file": len(file_warnings),
                "Unused variables": len(unused_var_warnings),
                "Missing docstrings": len(docstring_warnings),
            })

            results.append({
                "filename": file.filename,
                "function_length_graph": f"/graphs/{graph_filename}",
                "issues_pie_chart": f"/graphs/{pie_filename}"
            })

        except HTTPException as e:
            raise e
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })

    bar_filename = create_bar_chart(issues_per_file)

    return {
        "files": results,
        "issues_bar_chart": f"/graphs/{bar_filename}"
    }


