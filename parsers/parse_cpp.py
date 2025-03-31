# 📄 File: parse_cpp.py

import os
from tree_sitter import Language, Parser
from summarizers.summarize_function_cpp import summarize_cpp_function

CPP_LANGUAGE = Language("build/my-languages.so", "cpp")
parser = Parser()
parser.set_language(CPP_LANGUAGE)

def extract_structure(code, rel_path):
    tree = parser.parse(code)
    root = tree.root_node

    structure = {
        "file": rel_path,
        "language": "C++",
        "classes": [],
        "functions": []
    }

    def get_text(node):
        return code[node.start_byte:node.end_byte].decode(errors="ignore")

    def walk(node):
        if node.type == "function_definition":
            decl = node.child_by_field_name("declarator")
            name = get_text(decl) if decl else "anonymous"
            summary = summarize_cpp_function(get_text(node))
            structure["functions"].append({
                "name": name,
                "args": [],  # You can parse args from declarator if needed
                "doc": None,
                "summary": summary
            })

        elif node.type == "class_specifier":
            name_node = node.child_by_field_name("name")
            name = get_text(name_node) if name_node else "UnnamedClass"
            structure["classes"].append({
                "name": name,
                "bases": [],
                "methods": [],
                "doc": None
            })

        for child in node.children:
            walk(child)

    walk(root)
    return structure

def parse_all_cpp_files(base_dir, file_list):
    summaries = []
    for path in file_list:
        rel_path = os.path.relpath(path, base_dir)
        try:
            with open(path, "rb") as f:
                code = f.read()
            structure = extract_structure(code, rel_path)
            summaries.append(structure)
        except Exception as e:
            print(f"❌ Failed to parse {rel_path}: {e}")
    return summaries
