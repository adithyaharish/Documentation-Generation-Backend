# 📄 File: app.py

from flask import Flask, request, jsonify
from run_docgen_cli import run_docgen, run_docgen_for_existing_repo
import json
from flask_cors import CORS
from docgen_from_github import checkout_branch
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
CORS(app)

@app.route("/default-doc", methods=["POST"])
def generate_docs():
    data = request.get_json()
    repo_url = data.get("repo_url", "").strip()
    branch = data.get("branch", "").strip()

    if not repo_url:
        return jsonify({"error": "Missing repo_url"}), 400

    try:
        if branch:
            print(f"📦 Generating docs for branch: {branch}")
            result = run_docgen_for_existing_repo(branch)
        else:
            print(f"📦 Generating docs from URL: {repo_url}")
            result = run_docgen(repo_url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error":str(e)}),500
    

@app.route("/branch-doc", methods=["POST"])
def generate_docs_for_branch():
    data = request.get_json()
    branch = data.get("branch")

    if not branch:
        return jsonify({"error": "Missing branch"}), 400

    try:
        result = run_docgen_for_existing_repo(branch)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT", 5000))
