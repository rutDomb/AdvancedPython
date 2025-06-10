from fastapi import APIRouter,File,UploadFile
import ast
import os

router=APIRouter()


def check_function_length(tree):
    warnings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno
            end = max([n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')], default=start)
            length = end - start + 1
            if length > 20:
                warnings.append(f"Function '{node.name}' is too long: {length} lines")
    return warnings



def check_file_length(code_text: str):
    lines = code_text.splitlines()
    if len(lines) > 200:
        return [f"File is too long: {len(lines)} lines"]
    return []


def check_unused_variables(tree):
    assigned_vars = set()
    used_vars = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned_vars.add(target.id)
        elif isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                used_vars.add(node.id)
    unused_vars = assigned_vars - used_vars
    warnings = [f"Variable '{var}' is assigned but never used" for var in unused_vars]
    return warnings


def check_missing_docstrings(tree):
    warnings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if ast.get_docstring(node) is None:
                warnings.append(f"Function '{node.name}' is missing a docstring")
    return warnings
