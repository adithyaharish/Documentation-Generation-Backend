# 📄 File: summarize_function.py

import ast

def summarize_function_from_node(code, node):
    def get_text(n):
        return code[n.start_byte:n.end_byte].decode()

    # Step 1: Use docstring if available
    for child in node.children:
        if child.type == "expression_statement":
            string_node = child.children[0] if child.children else None
            if string_node and string_node.type == "string":
                return get_text(string_node).strip('"\'')

    # Step 2: Analyze function body using AST for keyword extraction
    try:
        fn_code = get_text(node)
        tree = ast.parse(fn_code)
        keywords = set()

        class Visitor(ast.NodeVisitor):
            def visit_Call(self, node):
                if isinstance(node.func, ast.Attribute):
                    keywords.add(node.func.attr.lower())
                elif isinstance(node.func, ast.Name):
                    keywords.add(node.func.id.lower())
                self.generic_visit(node)

            def visit_Str(self, node):
                keywords.add(node.s.lower())

        Visitor().visit(tree)

        # Map keywords to summaries
        keyword_map = {
            "jwt": "Handles JWT-based authentication",
            "decode": "Decodes encoded data or tokens",
            "token": "Processes authentication tokens",
            "db": "Interacts with database",
            "find": "Performs a database lookup",
            "query": "Executes a database query",
            "email": "Handles sending or reading emails",
            "request": "Processes incoming web requests",
            "response": "Generates API response",
            "plot": "Generates a visualization or plot",
            "cluster": "Applies clustering algorithm to data",
            "train": "Trains a machine learning model"
        }

        for kw in keyword_map:
            if any(kw in k for k in keywords):
                return keyword_map[kw]

    except Exception:
        pass  # Ignore AST errors silently

    # Step 3: Fallback to function name
    name_node = node.child_by_field_name("name")
    if name_node:
        func_name = get_text(name_node)
        tokens = func_name.replace("_", " ").split()
        if tokens:
            return f"Performs operation: {' '.join(tokens).capitalize()}"

    return "No summary available"
