# 📄 File: summarize_function_java.py

def summarize_java_function(code):
    code = code.strip()

    # Step 1: Use doc-comment if available
    lines = code.split("\n")
    for i, line in enumerate(lines):
        if line.strip().startswith("//") or line.strip().startswith("/*") or line.strip().startswith("*"):
            return line.strip().lstrip("/* ").rstrip("*/ ")

    # Step 2: Rule-based keyword extraction
    keyword_map = {
        "jwt": "Handles JWT-based authentication",
        "token": "Processes auth tokens",
        "decode": "Decodes encoded data",
        "database": "Interacts with database",
        "query": "Executes a DB query",
        "find": "Finds records in a DB",
        "email": "Handles sending or reading emails",
        "request": "Processes web request",
        "response": "Generates HTTP response",
        "http": "Handles HTTP operations",
        "connect": "Connects to external service",
        "fetch": "Fetches external data",
        "log": "Logs data or errors",
        "read": "Reads from file or stream",
        "write": "Writes to file or stream",
        "print": "Prints output",
        "render": "Renders UI elements",
        "calculate": "Performs a calculation",
        "validate": "Validates data or input",
        "cluster": "Applies clustering algorithm",
        "train": "Trains machine learning model",
        "initialize": "Initializes values or services"
    }

    matches = [v for k, v in keyword_map.items() if k in code.lower()]
    if matches:
        return f"Performs Java operation: {', '.join(set(matches))}."

    # Step 3: Fallback using method name
    try:
        line = lines[0]
        if "(" in line:
            name = line.split("(")[0].split()[-1]
            return f"Defines Java method '{name}' performing custom logic."
    except Exception:
        pass

    return "Performs a Java function or operation."
