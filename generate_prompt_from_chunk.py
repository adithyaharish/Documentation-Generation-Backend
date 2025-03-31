# 📄 File: generate_prompt_from_chunk.py
from pprint import pprint

def generate_prompt_from_chunk(chunk_structures):
    lines = [
    ]

    for file_summary in chunk_structures:
        lines.append(f"{file_summary['file']} ({file_summary.get('language', 'Unknown')})")

        if file_summary["classes"]:
            lines.append("Classes:")
            for cls in file_summary["classes"]:
                lines.append(f"- {cls['name']}" + (f" (inherits: {', '.join(cls['bases'])})" if cls['bases'] else ""))
                for method in cls["methods"]:
                    sig = f"{method['name']}({', '.join(method['args'])})"
                    doc = method.get("doc")
                    summary = method.get("summary")
                    if doc and summary:
                        lines.append(f"    - method: {sig} → {summary} | Doc: {doc}")
                    elif summary:
                        lines.append(f"    - method: {sig} → {summary}")
                    elif doc:
                        lines.append(f"    - method: {sig} → {doc}")
                    else:
                        lines.append(f"    - method: {sig} → No description")
        else:
            lines.append("Classes: None")

        if file_summary["functions"]:
            lines.append("Functions:")
            for func in file_summary["functions"]:
                sig = f"{func['name']}({', '.join(func['args'])})"
                doc = func.get("doc")
                summary = func.get("summary")
                if doc and summary:
                    lines.append(f"- {sig} → {summary} | Doc: {doc}")
                elif summary:
                    lines.append(f"- {sig} → {summary}")
                elif doc:
                    lines.append(f"- {sig} → {doc}")
                else:
                    lines.append(f"- {sig} → No description")
        else:
            lines.append("Functions: None")

        lines.append("")  # Spacer

    lines.append("Generate a clear and concise documentation explaining each file’s purpose, classes, functions, and how they fit together if applicable.")

    return "\n".join(lines)


# ✅ Usage Example (can go in another file like `run_prompt_generation.py`)

if __name__ == "__main__":
    from group_chunks import group_related_files
    from build_dependency_graph import build_dependency_graph
    import os
    from parse_all import parse_all_files
    from docgen_from_github import detect_languages,clone_repo
    from utils.file_filters import get_chunk_group_map, filter_chunks_with_gpt
    from run_docgen_cli import run_docgen, run_docgen_for_existing_repo
    from flask import jsonify

    result = (run_docgen("https://github.com/adithyaharish/pingpong-game-in-java"))
    import json
    print(json.dumps(result, indent=2))

    # github_url = input("🔗 Enter GitHub repo URL: ").strip()
    # repo = clone_repo(github_url)

    # files_by_language = detect_languages(repo)
    # dep_graph = build_dependency_graph(files_by_language, repo)

    # chunks, group_map = group_related_files(dep_graph)

    # print("\n📁 Detected Groups:")
    # for folder, files in group_map.items():
    #     print(f"{folder} = {files}")

    # # Step 2: Parse structure of all files
    # all_structures = parse_all_files(files_by_language, repo)
    # structure_lookup = {item["file"]: item for item in all_structures}

    # chunks = filter_chunks_with_gpt(chunks, structure_lookup)
    # print("chunks", chunks)

    # for chunk in chunks:
    #     print(chunk)
    #     chunk_structures = [structure_lookup[f] for f in chunk if f in structure_lookup]
    #     prompt = generate_prompt_from_chunk(chunk_structures)

    #     print("\nGPT Prompt for Chunk:")
    #     print(prompt)
    #     print("-" * 60)
