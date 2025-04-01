from tree_sitter import Language

Language.build_library(
    'build/my-languages.so',
    [
         'grammars/tree-sitter-python',   # Correct path to Python grammar
        'grammars/tree-sitter-javascript', # Correct path to JavaScript grammar
        'grammars/tree-sitter-java',      # Correct path to Java grammar
        'grammars/tree-sitter-cpp' 
    ]
)


print("✅ Build complete: build/my-languages.so")
