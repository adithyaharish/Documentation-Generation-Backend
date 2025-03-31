import os
from tree_sitter import Language, Parser
from summarizers.summarize_function import summarize_function_from_node

# Load compiled parser
PY_LANGUAGE = Language('build/my-languages.so', 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)

def extract_structure(code, rel_path):
    tree = parser.parse(code)
    root_node = tree.root_node

    structure = {
        "file": rel_path,
        "language": "Python",
        "classes": [],
        "functions": []
    }

    def get_text(node):
        return code[node.start_byte:node.end_byte].decode()

    def extract_args(param_node):
        args = []
        for child in param_node.children:
            if child.type == "identifier":
                args.append(get_text(child))
        return args

    def extract_decorators(node):
        decs = []
        for child in node.children:
            if child.type == "decorator":
                decs.append(get_text(child))
        return decs

    def extract_docstring(node):
        for child in node.children:
            if child.type == "expression_statement" and len(child.children) > 0:
                sub = child.children[0]
                if sub.type == "string":
                    return get_text(sub).strip('\"\'')
        return None

    def walk(node, inside_class=None):
        if node.type == "class_definition":
            name_node = node.child_by_field_name("name")
            class_name = get_text(name_node)

            bases = []
            super_node = node.child_by_field_name("superclasses")
            if super_node:
                for child in super_node.children:
                    if child.type == "identifier":
                        bases.append(get_text(child))

            class_info = {
                "name": class_name,
                "bases": bases,
                "methods": [],
                "doc": extract_docstring(node)
            }

            for child in node.children:
                walk(child, class_info)

            structure["classes"].append(class_info)

        elif node.type == "function_definition":
            name = get_text(node.child_by_field_name("name"))
            params = node.child_by_field_name("parameters")
            args = extract_args(params) if params else []

            method_info = {
                "name": name,
                "args": args,
                "decorators": extract_decorators(node),
                "doc": extract_docstring(node),
                "summary": summarize_function_from_node(code, node)
            }

            if inside_class:
                inside_class["methods"].append(method_info)
            else:
                structure["functions"].append(method_info)

        else:
            for child in node.children:
                walk(child, inside_class)

    walk(root_node)
    return structure


def parse_all_python_files(base_dir, file_list):

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

# ✅ Run the parser on the real repo
if __name__ == "__main__":
    import os

    repo_dir = "cloned_repo"
    py_files = [
        os.path.join(root, f)
        for root, _, files in os.walk(repo_dir)
        for f in files if f.endswith(".py")
    ]

    results = parse_all_python_files(repo_dir, py_files)

    from pprint import pprint
    for summary in results:
        print(f"\n📄 {summary['file']}")
        pprint(summary)

