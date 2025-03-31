# 📄 File: summarize_group_with_gpt.py

import openai
import os
import json
import re
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_files_with_gpt(chunks, structure_lookup, repo_dir):
    all_file_data = []

    # Force one file per chunk
    single_file_chunks = [{file} for chunk in chunks for file in chunk]

    for chunk in single_file_chunks:
        file = list(chunk)[0]
        file_path = os.path.join(repo_dir, file)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            all_file_data.append({"file": file, "code": code})
        except Exception as e:
            print(f"❌ Failed to read {file}: {e}")

    results = []
    batch_size = 10
    for i in range(0, len(all_file_data), batch_size):
        batch = all_file_data[i:i + batch_size]
        prompt = """You are an expert software engineer. I will give you a list of source code files along with their content. 

        Your task:
        For EACH file, write a concise 1-2 line high-level summary that describes the file’s overall purpose and what it does. Focus on *what the file accomplishes* or its role in the project.

        Return the result as a JSON array. Each item must include:
        - "file": string → the file path
        - "summary": string → the file-level summary

        Use this exact format:

        [
        {
            "file": "src/components/email.js",
            "summary": "Renders a vertical email link on the screen using styled-components. Used for contact visibility."
        },
        {
            "file": "src/pages/index.js",
            "summary": "Main landing page of the app with layout and section imports."
        }
        ]

        Here are the files and their contents:
        """


        for item in batch:
            prompt += f"\n--- FILE: {item['file']} ---\n{item['code']}\n"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert software engineer."},
                    {"role": "user", "content": prompt}
                ],
            )
            content = response["choices"][0]["message"]["content"].strip()
            start = content.find("[")
            end = content.rfind("]") + 1
            json_str = content[start:end]

            # 🔧 Remove trailing commas before closing brackets
            cleaned_json_str = re.sub(r",\s*]", "]", json_str)

            parsed = json.loads(cleaned_json_str,strict=False)

            # Match file-to-summary safely
            parsed_map = {
                entry["file"].replace("\\", "/"): entry.get("summary", "No content available")
                for entry in parsed
            }

            for f in batch:
                normalized = f["file"].replace("\\", "/")
                results.append({
                    "file": f["file"],
                    "summary": parsed_map.get(normalized, "No content available")
                })

        except Exception as e:
            print("❌ GPT summarization failed:", e)
            for f in batch:
                results.append({"file": f["file"], "summary": "No content available"})

    return results