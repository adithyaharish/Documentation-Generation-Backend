import os
import git
import shutil
from pathlib import Path
from collections import defaultdict
import stat
from utils.file_filters import is_excluded_path

GIT_CLONE_DIR = "./cloned_repo"

EXTENSION_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".rb": "Ruby",
    ".php": "PHP",
    ".rs": "Rust",
    ".ipynb": "Jupyter Notebook",
}

def handle_remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repo(repo_url, target_dir=GIT_CLONE_DIR):
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir, onerror=handle_remove_readonly)
    git.Repo.clone_from(repo_url, target_dir)
    print(f"✅ Repo cloned to {target_dir}")
    return target_dir


def detect_languages(repo_path):
    language_files = defaultdict(list)
    for root, _, files in os.walk(repo_path):
        for file in files:
            full_path = os.path.join(root, file)
            #  Skip junk/system/framework files
            if is_excluded_path(full_path):
                continue

            ext = Path(file).suffix
            lang = EXTENSION_MAP.get(ext)
            if lang:
                language_files[lang].append(full_path)
    return language_files

def get_repo_branches(repo_path):
    try:
        repo = git.Repo(repo_path)
        return [ref.name.replace("origin/", "") for ref in repo.remotes.origin.refs]
    except Exception:
        return []
    
    
def checkout_branch(repo_path, branch_name):
    repo = git.Repo(repo_path)
    repo.git.checkout(branch_name)
    print(f"✅ Checked out branch: {branch_name}")


if __name__ == "__main__":
    repo_url = input("Paste GitHub repo URL: ")
    clone_repo(repo_url)
    langs = detect_languages(GIT_CLONE_DIR)

    print("\n🧠 Detected Languages and Files:")
    for lang, files in langs.items():
        print(f"\n🔤 {lang} ({len(files)} files)")
        for f in files[:3]:
            print(f"  - {f}")
