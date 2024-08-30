import os


def print_tree(root, indent=""):
    files = [
        f for f in os.listdir(root) if f != ".venv" and f != "__pycache__" and f != ".git" and f != ".pytest_cache"
    ]
    for i, file in enumerate(files):
        path = os.path.join(root, file)
        if os.path.isdir(path):
            print(f"{indent}├── {file}/")
            print_tree(path, indent + "│   ")
        else:
            print(f"{indent}├── {file}")


print_tree(".")
