import os
from tree_sitter import Language, Parser
from summarizers.summarize_function_js import summarize_javascript_function

JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
parser = Parser()
parser.set_language(JS_LANGUAGE)

def extract_structure(code, rel_path):
    tree = parser.parse(code)
    root = tree.root_node

    structure = {
        "file": rel_path,
        "language": "JavaScript",
        "classes": [],
        "functions": []
    }

    def get_text(node):
        return code[node.start_byte:node.end_byte].decode()

    def walk(node):
        if node.type == "function_declaration":
            name = get_text(node.child_by_field_name("name"))
            params = node.child_by_field_name("parameters")
            args = []
            if params:
                args = [get_text(p) for p in params.children if p.type == "identifier"]
            structure["functions"].append({
                "name": name,
                "args": args,
                "doc": None,
                "summary": summarize_javascript_function(get_text(node))
            })

        elif node.type == "variable_declaration":
            for decl in node.children:
                if decl.type == "variable_declarator":
                    name_node = decl.child_by_field_name("name")
                    value_node = decl.child_by_field_name("value")
                    if value_node and value_node.type == "arrow_function":
                        name = get_text(name_node)
                        params = value_node.child_by_field_name("parameters")
                        args = []
                        if params:
                            args = [get_text(p) for p in params.children if p.type == "identifier"]
                        structure["functions"].append({
                            "name": name,
                            "args": args,
                            "doc": None,
                            "summary": summarize_javascript_function(get_text(decl))
                        })

        elif node.type == "lexical_declaration":
            for decl in node.children:
                if decl.type == "variable_declarator":
                    name_node = decl.child_by_field_name("name")
                    if name_node:
                        name = get_text(name_node)
                        structure["functions"].append({
                            "name": name,
                            "args": [],
                            "doc": None,
                            "summary": summarize_javascript_function(get_text(decl))
                        })

        elif node.type == "class_declaration":
            name = get_text(node.child_by_field_name("name"))
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

def parse_all_javascript_files(base_dir, file_list):
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