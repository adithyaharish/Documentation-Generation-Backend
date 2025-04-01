**Overview**
This project is a Documentation Generator that uses AI to create dynamic, interactive documentation from GitHub repositories. It allows users to generate documentation for various programming languages (e.g., Java, Python, JavaScript) and refine it using a conversation with AI. The tool supports multiple user levels (Beginner, Intermediate, Expert) and branch-wise documentation generation.

**Key Features**
Folder-like Structure Acceptance: The tool can process repositories with nested folder structures and automatically generate documentation for all project files.

Multiple Language Support: Supports generating documentation for various languages, such as Java, Python, and JavaScript.

Branch-wise Documentation: Users can generate documentation for specific branches in a GitHub repository.

Persona-based Levels: The system generates documentation based on the user's expertise level (Beginner, Intermediate, or Expert).

AI-based Chat Interface: Users can refine and ask questions about the generated documentation through a chat interface with AI.

**Project Structure**

Frontend
src/App.js: Main React component that manages the user interface and handles user interactions for generating documentation and refining it through the chat.

src/components/DocumentationPanel.js: Displays the generated documentation in a clean and user-friendly format.

src/components/ChatInterface.js: Handles the AI chat interface where users can refine and ask questions about the generated documentation.

Backend (Flask)

app.py: The Flask backend that handles API requests. It generates documentation by interacting with OpenAI’s API and processes user messages for refining documentation.

code_dox.py: Contains logic for extracting project structure and generating summaries for each file in the repository.

Running the Project
Prerequisites
Python 3.x

Node.js (for React frontend)

OpenAI API Key (for generating documentation via GPT)


**
Backend Setup:**

Install Python dependencies:

pip install -r requirements.txt
Run the Flask server:
python app.py


**Frontend Setup:**

Navigate to the frontend directory:


Install Node.js dependencies:
npm install
Start the React development server:
npm start

**Accessing the App:**

Visit http://localhost:3000 in your browser to interact with the documentation generator and AI chat.

**Libraries and Frameworks Used**

Frontend: React, React Router

Backend: Flask, OpenAI API, Requests


This prototype demonstrates an innovative approach to documentation generation, utilizing AI to not only generate summaries but also enhance them interactively with human-AI conversation. It provides a dynamic, flexible, and user-friendly experience for developers working with diverse codebases.
