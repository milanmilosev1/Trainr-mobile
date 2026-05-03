"""
Parses app/main.py to discover all registered FastAPI routers, then
re-generates the <!-- ROUTERS_START --> … <!-- ROUTERS_END --> section in
README.md.

Run manually:
    python scripts/update_readme.py

Or let .github/workflows/update-readme.yml run it automatically on every
push that touches app/main.py or any app/**/router.py.
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_PY = os.path.join(REPO_ROOT, "app", "main.py")
README_PATH = os.path.join(REPO_ROOT, "README.md")

ROUTERS_START = "<!-- ROUTERS_START -->"
ROUTERS_END = "<!-- ROUTERS_END -->"

# HTTP methods supported by FastAPI routers
HTTP_METHODS = ("get", "post", "put", "patch", "delete")


def get_router_modules() -> list[str]:
    """
    Parse app/main.py and return file paths for every included router,
    in the order they appear in the file.
    """
    with open(MAIN_PY, encoding="utf-8") as fh:
        content = fh.read()

    # Match aliased imports:   from app.X.router import router as some_alias
    aliased_re = re.compile(r"from\s+(app(?:\.\w+)+)\s+import\s+router\s+as\s+(\w+)")
    alias_to_module: dict[str, str] = {}
    for module_path, alias in aliased_re.findall(content):
        alias_to_module[alias] = module_path

    # Match bare imports:      from app.X.router import router
    # Use the last component of the module path as the de-facto alias ("router"),
    # but only when the name isn't already claimed by an aliased import.
    bare_re = re.compile(r"from\s+(app(?:\.\w+)+)\s+import\s+router(?!\s+as\s+\w)")
    for (module_path,) in bare_re.findall(content):
        alias_to_module.setdefault("router", module_path)

    # Match: app.include_router(some_alias)
    include_re = re.compile(r"app\.include_router\(\s*(\w+)\s*\)")
    file_paths: list[str] = []
    for alias in include_re.findall(content):
        module_path = alias_to_module.get(alias)
        if module_path:
            file_path = os.path.join(REPO_ROOT, module_path.replace(".", os.sep) + ".py")
            if os.path.isfile(file_path):
                file_paths.append(file_path)
            else:
                print(f"Warning: router file not found: {file_path}")

    return file_paths


def parse_router_file(file_path: str) -> dict:
    """
    Parse a router.py file and return a dict with:
      - tag      : display name (from APIRouter tags=)
      - prefix   : URL prefix  (from APIRouter prefix=)
      - endpoints: list of (method, path, func_name)
    """
    with open(file_path, encoding="utf-8") as fh:
        content = fh.read()

    # Extract prefix and first tag from APIRouter(...).
    # Walk character-by-character to handle nested parentheses correctly.
    prefix = ""
    tag = os.path.basename(os.path.dirname(file_path)).capitalize()
    api_router_start = re.search(r'APIRouter\s*\(', content)
    decl = ""
    if api_router_start:
        depth = 1
        i = api_router_start.end()
        while i < len(content) and depth:
            ch = content[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if depth:
                decl += ch
            i += 1
    if decl:
        prefix_m = re.search(r'prefix\s*=\s*["\']([^"\']*)["\']', decl)
        if prefix_m:
            prefix = prefix_m.group(1)
        tag_m = re.search(r'tags\s*=\s*\[\s*["\']([^"\']+)["\']', decl)
        if tag_m:
            tag = tag_m.group(1)

    # Extract endpoint decorators + function names
    # Handles multi-line decorators by using DOTALL up to the `def` keyword
    endpoint_re = re.compile(
        r'@router\.(' + '|'.join(HTTP_METHODS) + r')\s*\(\s*["\']([^"\']*)["\'].*?\)\s*\ndef\s+(\w+)',
        re.DOTALL,
    )
    endpoints = [
        (method.upper(), path, func_name)
        for method, path, func_name in endpoint_re.findall(content)
    ]

    return {"tag": tag, "prefix": prefix, "endpoints": endpoints}


def func_name_to_description(func_name: str) -> str:
    """Convert a snake_case function name to a human-readable description."""
    return func_name.replace("_", " ").capitalize()


def generate_section(router_info: dict) -> str:
    """Return a markdown string for one router group."""
    lines = [
        f"### {router_info['tag']}",
        "",
        f"**Base path:** `{router_info['prefix']}`",
        "",
        "| Method | Path | Description |",
        "|--------|------|-------------|",
    ]
    for method, path, func_name in router_info["endpoints"]:
        full_path = router_info["prefix"] + path
        description = func_name_to_description(func_name)
        lines.append(f"| `{method}` | `{full_path}` | {description} |")
    return "\n".join(lines)


def update_readme(new_content: str) -> None:
    """Replace the content between the ROUTERS_START / ROUTERS_END markers."""
    with open(README_PATH, encoding="utf-8") as fh:
        readme = fh.read()

    start_idx = readme.find(ROUTERS_START)
    end_idx = readme.find(ROUTERS_END)

    if start_idx == -1 or end_idx == -1:
        print("ERROR: Could not find router markers in README.md – aborting.")
        return

    updated = (
        readme[: start_idx + len(ROUTERS_START)]
        + "\n\n"
        + new_content
        + "\n\n"
        + readme[end_idx:]
    )

    with open(README_PATH, "w", encoding="utf-8") as fh:
        fh.write(updated)

    print("README.md updated successfully.")


def main() -> None:
    router_files = get_router_modules()
    if not router_files:
        print("No routers found in app/main.py – nothing to update.")
        return

    sections = []
    for file_path in router_files:
        info = parse_router_file(file_path)
        sections.append(generate_section(info))

    update_readme("\n\n".join(sections))


if __name__ == "__main__":
    main()
