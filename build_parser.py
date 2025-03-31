from tree_sitter import Language

Language.build_library(
    'build/my-languages.so',
    [
        'grammars/python',
        'grammars/javascript',
        'grammars/java',
        'grammars/cpp'
    ]
)


print("✅ Build complete: build/my-languages.so")
