# 📄 File: run_docgen_cli.py

from group_chunks import group_related_files
from build_dependency_graph import build_dependency_graph
from parse_all import parse_all_files
from docgen_from_github import checkout_branch, detect_languages, clone_repo, get_repo_branches
from utils.file_filters import filter_chunks_with_gpt, get_chunk_group_map, convert_chunks_to_list_of_sets
from generate_prompt_from_chunk import generate_prompt_from_chunk
from summarizers.summarize_group_with_gpt import summarize_files_with_gpt

def run_docgen(github_url):
    #github_url = input("🔗 Enter GitHub repo URL: ").strip()
    repo = clone_repo(github_url)
    branches = get_repo_branches(repo)

    files_by_language = detect_languages(repo)
    dep_graph = build_dependency_graph(files_by_language, repo)

    chunks, group_map = group_related_files(dep_graph)


    all_structures = parse_all_files(files_by_language, repo)
    structure_lookup = {item["file"]: item for item in all_structures}

    chunks = filter_chunks_with_gpt(chunks, structure_lookup)

    gpt_summaries = summarize_files_with_gpt(chunks, structure_lookup, repo)
    gpt_summary_map = {
    entry["file"].replace("\\", "/"): entry.get("summary", "No content available")
    for entry in gpt_summaries
    }


    summaries = []
    json_chunks = []

    for chunk in chunks:
        chunk_files = list(chunk)
        json_chunks.append(chunk_files)
        chunk_structures = [structure_lookup[f] for f in chunk_files if f in structure_lookup]
        
        try:
            prompt = generate_prompt_from_chunk(chunk_structures)
            pretty_prompt = "\n".join(line.strip() for line in prompt.strip().split("\n"))
        except Exception as e:
            pretty_prompt = "No content available"

        # Attach 1-line summary if available
        oneline_summary = None
        if len(chunk_files) == 1:
            normalized_file = chunk_files[0].replace("\\", "/")
            oneline_summary = gpt_summary_map.get(normalized_file, "No content available")


        summaries.append({
            "file": chunk_files,
            "summary": pretty_prompt,
            "oneline": oneline_summary
        })

    output = {
        "branches": branches,
        "chunks": json_chunks,
        "groups": group_map,
        "summaries": summaries
    }

    return output


def run_docgen_for_existing_repo(branch_name):

    repo_path = "cloned_repo"

    # ✅ Switch to the specified branch
    checkout_branch(repo_path, branch_name)

    files_by_language = detect_languages(repo_path)
    dep_graph = build_dependency_graph(files_by_language, repo_path)
    chunks, group_map = group_related_files(dep_graph)

    all_structures = parse_all_files(files_by_language, repo_path)
    structure_lookup = {item["file"]: item for item in all_structures}

    chunks = filter_chunks_with_gpt(chunks, structure_lookup)

    gpt_summaries = summarize_files_with_gpt(chunks, structure_lookup, repo_path)
    gpt_summary_map = {
        entry["file"].replace("\\", "/"): entry.get("summary", "No content available")
        for entry in gpt_summaries
    }

    summaries = []
    json_chunks = []

    for chunk in chunks:
        chunk_files = list(chunk)
        json_chunks.append(chunk_files)
        chunk_structures = [structure_lookup[f] for f in chunk_files if f in structure_lookup]

        try:
            prompt = generate_prompt_from_chunk(chunk_structures)
            pretty_prompt = "\n".join(line.strip() for line in prompt.strip().split("\n"))
        except Exception as e:
            pretty_prompt = "No content available"

        # Attach 1-line summary if available
        oneline_summary = None
        if len(chunk_files) == 1:
            normalized_file = chunk_files[0].replace("\\", "/")
            oneline_summary = gpt_summary_map.get(normalized_file, "No content available")

        summaries.append({
            "file": chunk_files,
            "summary": pretty_prompt,
            "oneline": oneline_summary
        })

    return {
        "branch_used": branch_name,
        "chunks": json_chunks,
        "groups": group_map,
        "summaries": summaries
    }
