# Use an official lightweight Python image
FROM --platform=linux/amd64 python:3.10-slim
# FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (needed for Tree-sitter)
RUN apt-get update && apt-get install -y \
    gcc git make build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (to optimize caching)
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Clone and build Tree-sitter languages
RUN mkdir -p /app/build /app/tree-sitter-languages \
    && cd /app/tree-sitter-languages \
    && git clone https://github.com/tree-sitter/tree-sitter-python \
    && git clone https://github.com/tree-sitter/tree-sitter-javascript \
    && git clone https://github.com/tree-sitter/tree-sitter-java \
    && git clone https://github.com/tree-sitter/tree-sitter-cpp \
    && echo "Cloned repositories" \
    && ls -la \
    && gcc -shared -o /app/build/my-languages.so -fPIC \
    tree-sitter-python/src/parser.c tree-sitter-python/src/scanner.c \
    tree-sitter-javascript/src/parser.c tree-sitter-javascript/src/scanner.c \
    tree-sitter-java/src/parser.c \
    tree-sitter-cpp/src/parser.c tree-sitter-cpp/src/scanner.c \
    -I tree-sitter-python/src \
    -I tree-sitter-javascript/src \
    -I tree-sitter-java/src \
    -I tree-sitter-cpp/src \
    -Wl,-soname,my-languages.so \
    && echo "Compilation complete" \
    && rm -rf /app/tree-sitter-languages  # Cleanup

# RUN ls -lah /app/build/ && file /app/build/my-languages.so

# Copy the rest of the app code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Set the default command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
# CMD ["bash"]
