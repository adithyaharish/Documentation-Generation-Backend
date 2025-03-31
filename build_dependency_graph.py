# 📄 File: build_dependency_graph.py

import os
from collections import defaultdict
from tree_sitter import Language, Parser

# Map language names to their Tree-sitter identifiers
LANGUAGE_IDENTIFIERS = {
    "Python": "python",
    "JavaScript": "javascript",
    "Java": "java",
    "C++": "cpp",
    # Add more as needed
}

# Load languages into parser map
SO_PATH = 'build/my-languages.so'
PARSER_MAP = {}
for lang_name, tree_sitter_id in LANGUAGE_IDENTIFIERS.items():
    lang = Language(SO_PATH, tree_sitter_id)
    parser = Parser()
    parser.set_language(lang)
    PARSER_MAP[lang_name] = parser

def build_dependency_graph(files_by_language, base_dir):
    graph = defaultdict(list)
    all_files_set = set()

    # Flatten file list and build file set
    for files in files_by_language.values():
        for path in files:
            rel_path = os.path.relpath(path, base_dir)
            all_files_set.add(rel_path)
            graph[rel_path] = []  # Initialize node in graph

    def extract_imports(code_bytes, lang):
        parser = PARSER_MAP.get(lang)
        if not parser:
            return []

        tree = parser.parse(code_bytes)
        root = tree.root_node
        imports = []

        def walk(node):
            if lang == "Python":
                if node.type == "import_statement":
                    for child in node.children:
                        if child.type == "dotted_name":
                            imports.append(code_bytes[child.start_byte:child.end_byte].decode())
                elif node.type == "import_from_statement":
                    module = node.child_by_field_name("module")
                    if module:
                        imports.append(code_bytes[module.start_byte:module.end_byte].decode())
            elif lang == "JavaScript":
                if node.type == "import_statement":
                    source = node.child_by_field_name("source")
                    if source:
                        val = code_bytes[source.start_byte:source.end_byte].decode().strip("'\"")
                        imports.append(val)
            elif lang == "Java":
                if node.type == "import_declaration":
                    imports.append(code_bytes[node.start_byte:node.end_byte].decode())
            elif lang == "C++":
                if node.type == "preproc_include":
                    raw = code_bytes[node.start_byte:node.end_byte].decode()
                    if '"' in raw:
                        imports.append(raw.split('"')[1])
                    elif '<' in raw:
                        imports.append(raw.split('<')[1].split('>')[0])
            for child in node.children:
                walk(child)

        walk(root)
        return imports

    def resolve_module_to_file(module_name, file_dir, base_dir, all_files_set):
        parts = module_name.replace("/", ".").replace("\\", ".").split(".")
        candidate = os.path.join(base_dir, *parts) + ".py"
        rel_path = os.path.relpath(candidate, base_dir)
        if rel_path in all_files_set:
            return rel_path

        alt_path = os.path.join(file_dir, *parts) + ".py"
        rel_alt = os.path.relpath(alt_path, base_dir)
        if rel_alt in all_files_set:
            return rel_alt

        return None

    # Loop through all files and resolve dependencies
    for lang, files in files_by_language.items():
        for path in files:
            rel_path = os.path.relpath(path, base_dir)
            file_dir = os.path.dirname(path)
            try:
                with open(path, "rb") as f:
                    code = f.read()
                raw_imports = extract_imports(code, lang)

                for imp in raw_imports:
                    resolved = resolve_module_to_file(imp, file_dir, base_dir, all_files_set)
                    if resolved:
                        graph[rel_path].append(resolved)
            except Exception:
                pass

    return dict(graph)


# ✅ Test Entry Point
if __name__ == "__main__":
    from docgen_from_github import detect_languages
    import pprint

    repo = "cloned_repo"
    files_by_language = detect_languages(repo)
    dep_graph = build_dependency_graph(files_by_language, repo)

    print("\n🧠 Final Dependency Graph:")
    pprint.pprint(dep_graph)
