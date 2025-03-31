from parsers.parse_python import parse_all_python_files
from parsers.parse_javascript import parse_all_javascript_files
from parsers.parse_cpp import parse_all_cpp_files
from parsers.parse_java import parse_all_java_files

def parse_all_files(files_by_language, base_dir):
    results = []

    if "Python" in files_by_language:
        results += parse_all_python_files(base_dir, files_by_language["Python"])

    if "JavaScript" in files_by_language:
        results += parse_all_javascript_files(base_dir, files_by_language["JavaScript"])

    if "C++" in files_by_language:
        results += parse_all_cpp_files(base_dir, files_by_language["C++"])
    
    if "Java" in files_by_language:  # ✅ Add this block
        results += parse_all_java_files(base_dir, files_by_language["Java"])

    # You’ll add more like parse_javascript.py etc later
    return results
