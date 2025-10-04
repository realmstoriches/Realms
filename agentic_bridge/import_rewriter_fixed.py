import os, ast, logging

ROOT = r"F:\Realms"
LOG = os.path.join(ROOT, "logs", "import_rewrite.log")
logging.basicConfig(filename=LOG, level=logging.INFO)

def rewrite_path(old):
    if not old: return None
    if "realms_core_alpha" in old or "realms_core_beta" in old: return "agents"
    if "promptgen" in old: return "tools.promptgen"
    if "executor" in old: return "core.executor"
    return old

def rewrite_imports():
    for root, _, files in os.walk(ROOT):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                    lines = []
                    for node in tree.body:
                        if isinstance(node, ast.ImportFrom) and node.module:
                            new_mod = rewrite_path(node.module)
                            if new_mod:
                                lines.append(f"from {new_mod} import {', '.join(n.name for n in node.names)}")
                        elif isinstance(node, ast.Import):
                            lines.append(f"import {', '.join(n.name for n in node.names)}")
                    if lines:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write("\n".join(lines))
                except Exception as e:
                    logging.info(f"⚠️ Failed to rewrite {path}: {e}")

if __name__ == "__main__":
    rewrite_imports()