# 📄 File: parse_java.py

import os
from tree_sitter import Language, Parser
from summarizers.summarize_function_java import summarize_java_function

JAVA_LANGUAGE = Language('build/my-languages.so', 'java')
parser = Parser()
parser.set_language(JAVA_LANGUAGE)

def extract_structure(code, rel_path):
    tree = parser.parse(code)
    root = tree.root_node

    structure = {
        "file": rel_path,
        "language": "Java",
        "classes": [],
        "functions": []
    }

    def get_text(node):
        return code[node.start_byte:node.end_byte].decode()

    def walk(node, inside_class=None):
        if node.type == "class_declaration":
            name_node = node.child_by_field_name("name")
            class_name = get_text(name_node)

            class_info = {
                "name": class_name,
                "bases": [],
                "methods": [],
                "doc": None
            }

            for child in node.children:
                walk(child, class_info)

            structure["classes"].append(class_info)

        elif node.type in ["method_declaration", "constructor_declaration"]:
            name_node = node.child_by_field_name("name")
            if name_node is None:
                return
            method_name = get_text(name_node)

            param_node = node.child_by_field_name("parameters")
            args = []
            if param_node:
                for p in param_node.children:
                    if p.type == "identifier":
                        args.append(get_text(p))

            method_info = {
                "name": method_name,
                "args": args,
                "doc": None,
                "summary": summarize_java_function(get_text(node))
            }

            if inside_class:
                inside_class["methods"].append(method_info)
            else:
                structure["functions"].append(method_info)

        for child in node.children:
            walk(child, inside_class)

    walk(root)
    return structure


def parse_all_java_files(base_dir, file_list):
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
