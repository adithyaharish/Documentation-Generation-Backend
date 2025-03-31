# 📄 File: summarize_function_js.py

def summarize_javascript_function(code):
    code = code.strip()

    # Step 1: If comment exists above function, return that
    lines = code.split("\n")
    for i, line in enumerate(lines):
        if line.strip().startswith("//") or line.strip().startswith("/*"):
            return line.strip().lstrip("/* ").rstrip("*/ ")

    # Step 2: Detect export constants
    if "export const" in code and ("[" in code or "{" in code):
        return "Exports a data array or configuration object."

    # Step 3: Extract keywords to infer purpose
    keywords = {
        "render": "Renders UI component",
        "map": "Iterates over a list",
        "filter": "Filters a list",
        "fetch": "Fetches data",
        "axios": "Performs HTTP request",
        "useState": "Manages React component state",
        "useEffect": "Handles side effects in React",
        "addEventListener": "Handles browser event listeners",
        "setTimeout": "Sets a delayed function execution",
        "localStorage": "Interacts with browser local storage",
        "JSON.parse": "Parses JSON string",
        "console.log": "Logs debug info"
    }

    matched = [v for k, v in keywords.items() if k in code]
    if matched:
        summary = ", ".join(set(matched))
        return f"Performs JavaScript function: {summary}."

    # Step 4: Use function name or fallback
    if "function " in code:
        name = code.split("function ")[1].split("(")[0].strip()
        return f"Defines function '{name}' performing custom logic."
    elif "const " in code and "=>" in code:
        name = code.split("const ")[1].split("=")[0].strip()
        return f"Defines arrow function '{name}' performing UI or logic."

    return "Performs a JavaScript operation."
