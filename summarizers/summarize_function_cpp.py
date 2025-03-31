# 📄 File: summarize_function_cpp.py

import re

# Enhanced summarizer that combines all available signals

def summarize_cpp_function(code_text):
    # Step 1: Try to extract doc-style comment (/** ... */)
    docstring = ""
    docstring_match = re.search(r"/\*\*(.*?)\*/", code_text, re.DOTALL)
    if docstring_match:
        docstring = docstring_match.group(1).strip()

    # Step 2: Try to extract inline comment (// ...)
    inline_comment = ""
    inline_match = re.search(r"//\s*(.+)", code_text)
    if inline_match:
        inline_comment = inline_match.group(1).strip()

    # Step 3: Extract function name as fallback
    function_name = "UnknownFunction"
    name_match = re.search(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*?\)", code_text)
    if name_match:
        function_name = name_match.group(1).replace("_", " ").capitalize()

    # Step 4: Collect all matched keywords for richer summary
    keyword_map = {
        "malloc": "dynamic memory allocation",
        "free": "memory deallocation",
        "new": "object instantiation",
        "delete": "object deletion",
        "std::cout": "console output",
        "std::cin": "console input",
        "cin": "console input",
        "cout": "console output",
        "ifstream": "file input",
        "ofstream": "file output",
        "fstream": "file handling",
        "vector": "dynamic array operations",
        "map": "key-value storage",
        "unordered_map": "hash map storage",
        "set": "unique collection handling",
        "stack": "stack-based logic",
        "queue": "queue-based logic",
        "deque": "double-ended queue",
        "sort": "sorting algorithms",
        "binary_search": "searching algorithm",
        "printf": "formatted output",
        "scanf": "formatted input",
        "chrono": "performance timing",
        "thread": "multi-threading",
        "mutex": "synchronization",
        "lock_guard": "thread-safe locking",
        "template": "generic programming",
        "class": "object-oriented design",
        "struct": "data structure definition",
        "namespace": "modular encapsulation"
    }

    lowered = code_text.lower()
    matched_keywords = [desc for key, desc in keyword_map.items() if key in lowered]

    # Combine everything into a comprehensive summary
    summary_parts = []

    if docstring:
        summary_parts.append(docstring)
    elif inline_comment:
        summary_parts.append(inline_comment)

    summary_parts.append(f"Function name: {function_name}")

    if matched_keywords:
        summary_parts.append("This function involves: " + ", ".join(sorted(set(matched_keywords))))

    return " | ".join(summary_parts).strip() or "No summary available"
