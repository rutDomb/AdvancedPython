from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import matplotlib.pyplot as plt
import ast
import os
import uuid


UPLOAD_DIR = "graphs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def extract_function_lengths(code_text):
    tree = ast.parse(code_text)
    lengths = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno
            end_line = max((child.lineno for child in ast.walk(node) if hasattr(child, 'lineno')), default=start_line)
            lengths.append(end_line - start_line + 1)
    return lengths


def create_histogram(lengths):
    plt.figure(figsize=(6,4))
    plt.hist(lengths, bins=10, color="skyblue", edgecolor="black")
    plt.title("Distribution of function lengths")
    plt.xlabel("Number of lines")
    plt.ylabel("Number of functions")
    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join(UPLOAD_DIR, filename)
    print(filepath)
    plt.savefig(filepath)
    plt.close()
    return filename


def create_pie_chart(issue_counts: dict):
    labels = list(issue_counts.keys())
    sizes = list(issue_counts.values())

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Problem percentages")

    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join(UPLOAD_DIR, filename)
    plt.savefig(filepath)
    plt.close()
    return filename


def create_bar_chart(issue_counts: dict):
    filenames = list(issue_counts.keys())
    counts = list(issue_counts.values())

    plt.figure(figsize=(8, 5))
    plt.bar(filenames, counts, color='coral', edgecolor='black')
    plt.xlabel('File Name')
    plt.ylabel('Total Issues')
    plt.title('Total Issues per File')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join(UPLOAD_DIR, filename)
    plt.savefig(filepath)
    plt.close()
    return filename