# 📄 File: group_chunks.py

from collections import defaultdict, deque
import os


def get_chunk_group_map(chunks):
    """
    Return grouped chunk structure as a dict.
    Example: {'src/utils': ['index.js', 'sr.js']}
    Automatically groups by deepest shared folder.
    """
    group_map = defaultdict(list)

    for chunk in chunks:
        for file in chunk:
            path_parts = file.replace("\\", "/").split("/")
            if len(path_parts) > 1:
                folder = "/".join(path_parts[:-1])  # all parts except filename
            else:
                folder = "root"
            filename = path_parts[-1]
            group_map[folder].append(filename)

    return dict(group_map)


def group_related_files(dep_graph):
    visited = set()
    chunks = []

    # Step 1: Group by explicit code dependencies (BFS traversal)
    for file in dep_graph:
        if file in visited:
            continue

        chunk = set()
        queue = deque([file])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            chunk.add(current)
            for neighbor in dep_graph.get(current, []):
                if neighbor not in visited:
                    queue.append(neighbor)

        if chunk:
            chunks.append(chunk)

    # ✅ Track all grouped files so far
    already_grouped = set().union(*chunks)

    # Step 2: Group remaining ungrouped files by folder structure
    ungrouped = set(dep_graph.keys()) - already_grouped
    folder_map = defaultdict(list)

    for file in ungrouped:
        if file in already_grouped:
            continue
        folder = os.path.dirname(file)
        folder_map[folder].append(file)

    for files in folder_map.values():
        group = set(files)
        if not group.issubset(already_grouped):
            chunks.append(group)
            already_grouped.update(group)

    # Step 3: Group by component name (React convention — same prefix before dot)
    prefix_map = defaultdict(list)
    all_files = set(dep_graph.keys())
    for file in all_files:
        if file in already_grouped:
            continue
        base = os.path.basename(file)
        prefix = base.split(".")[0]  # 'footer' from 'footer.js', 'footer.elements.js'
        path_root = os.path.dirname(file)
        key = f"{path_root}/{prefix}"
        prefix_map[key].append(file)

    for files in prefix_map.values():
        group = set(files)
        if not group.issubset(already_grouped):
            chunks.append(group)
            already_grouped.update(group)

    # Step 4: Group any remaining files by deepest folder path
    folder_group_map = defaultdict(list)
    for file in all_files:
        if file in already_grouped:
            continue
        folder = os.path.dirname(file).replace("\\", "/")
        folder_group_map[folder].append(file)

    for group in folder_group_map.values():
        if len(group) > 1:
            chunk = set(group)
            chunks.append(chunk)
            already_grouped.update(chunk)

    group_map = get_chunk_group_map(chunks)
    return chunks, group_map
