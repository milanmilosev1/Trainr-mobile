"""
Parses app/main.py to discover all registered FastAPI routers and re-generates
three auto-managed sections in README.md:

  <!-- ROUTERS_START -->          … <!-- ROUTERS_END -->
  <!-- PROJECT_STRUCTURE_START --> … <!-- PROJECT_STRUCTURE_END -->
  <!-- DATA_MODELS_START -->       … <!-- DATA_MODELS_END -->

Run manually:
    python scripts/update_readme.py

Or let .github/workflows/update-readme.yml run it automatically on every
push that touches app/main.py, any app/**/router.py, or any app/**/models.py.
"""

import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(REPO_ROOT, "app")
MAIN_PY = os.path.join(APP_DIR, "main.py")
README_PATH = os.path.join(REPO_ROOT, "README.md")

ROUTERS_START = "<!-- ROUTERS_START -->"
ROUTERS_END = "<!-- ROUTERS_END -->"
PROJECT_STRUCTURE_START = "<!-- PROJECT_STRUCTURE_START -->"
PROJECT_STRUCTURE_END = "<!-- PROJECT_STRUCTURE_END -->"
DATA_MODELS_START = "<!-- DATA_MODELS_START -->"
DATA_MODELS_END = "<!-- DATA_MODELS_END -->"

# HTTP methods supported by FastAPI routers
HTTP_METHODS = ("get", "post", "put", "patch", "delete")

# Descriptions for well-known file names (models.py is handled dynamically)
FILE_DESCRIPTIONS: dict[str, str] = {
    "db_connection.py": "Database engine, session factory, and Base",
    "main.py": "FastAPI app entry point; registers all routers",
    "schemas.py": "Pydantic DTOs",
    "repository.py": "Data access layer",
    "service.py": "Business logic",
    "router.py": "FastAPI route handlers",
}


# ---------------------------------------------------------------------------
# API Endpoints (routers)
# ---------------------------------------------------------------------------

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


def generate_routers_section(router_info: dict) -> str:
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


# ---------------------------------------------------------------------------
# Project Structure
# ---------------------------------------------------------------------------

def _get_model_class_name(file_path: str) -> str:
    """Return the first SQLAlchemy model class name found in a models.py file."""
    try:
        with open(file_path, encoding="utf-8") as fh:
            content = fh.read()
    except OSError:
        return ""
    m = re.search(r'^class\s+(\w+)\s*\(\s*Base\s*\)', content, re.MULTILINE)
    return m.group(1) if m else ""


def generate_project_structure() -> str:
    """Return a markdown code block containing the app/ directory tree."""

    def get_file_description(full_path: str, filename: str) -> str:
        if filename == "models.py":
            class_name = _get_model_class_name(full_path)
            return f"{class_name} SQLAlchemy model" if class_name else "SQLAlchemy models"
        return FILE_DESCRIPTIONS.get(filename, "")

    def build_tree(directory: str, prefix: str = "") -> list[str]:
        try:
            all_entries = sorted(os.listdir(directory))
        except PermissionError:
            return []
        entries = [
            e for e in all_entries
            if e != "__pycache__" and e != "__init__.py" and not e.endswith(".pyc")
        ]
        dirs = [e for e in entries if os.path.isdir(os.path.join(directory, e))]
        files = [e for e in entries if os.path.isfile(os.path.join(directory, e))]
        ordered = dirs + files

        lines = []
        for i, entry in enumerate(ordered):
            is_last = i == len(ordered) - 1
            connector = "└── " if is_last else "├── "
            full_path = os.path.join(directory, entry)

            if os.path.isdir(full_path):
                lines.append(f"{prefix}{connector}{entry}/")
                child_prefix = prefix + ("    " if is_last else "│   ")
                lines.extend(build_tree(full_path, child_prefix))
            else:
                desc = get_file_description(full_path, entry)
                if desc:
                    lines.append(f"{prefix}{connector}{entry}   # {desc}")
                else:
                    lines.append(f"{prefix}{connector}{entry}")
        return lines

    lines = ["```", "app/"]
    lines.extend(build_tree(APP_DIR))
    lines.append("```")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

def _parse_enum_values(content: str) -> dict[str, list[str]]:
    """Return a mapping of enum class name → list of member names."""
    enum_values: dict[str, list[str]] = {}
    enum_re = re.compile(
        r'^class\s+(\w+)\s*\(\s*(?:\w+\.)?Enum\s*\)\s*:\s*\n'
        r'((?:[ \t]+\w+\s*=\s*\S+[ \t]*\n?)+)',
        re.MULTILINE,
    )
    for enum_name, body in enum_re.findall(content):
        values = re.findall(r'^\s+(\w+)\s*=', body, re.MULTILINE)
        enum_values[enum_name] = values
    return enum_values


def _parse_col_type(
    mapped_type: str,
    col_args: str,
    enum_values: dict[str, list[str]],
) -> str:
    """Convert a Mapped[X] type annotation and column args to a readable type string."""
    mapped_type = mapped_type.strip()

    # String(N) in col_args takes precedence over the bare 'str' annotation
    str_n = re.search(r'\bString\s*\(\s*(\d+)\s*\)', col_args)
    if str_n and mapped_type == "str":
        return f"string({str_n.group(1)})"

    type_map = {
        "uuid.UUID": "UUID",
        "UUID": "UUID",
        "str": "string",
        "int": "int",
        "bool": "bool",
        "datetime": "datetime",
        "list[str]": "list[string]",
    }
    if mapped_type in type_map:
        return type_map[mapped_type]

    if mapped_type in enum_values:
        vals = ", ".join(f"`{v}`" for v in enum_values[mapped_type])
        return f"enum ({vals})"

    return mapped_type


def _parse_col_notes(col_args: str) -> str:
    """Parse mapped_column() arguments into human-readable notes."""
    parts = []

    if "primary_key=True" in col_args:
        note = "primary key"
        if re.search(r'\bdefault\s*=\s*uuid\.uuid4\b', col_args):
            note += ", auto-generated"
        parts.append(note)

    if "unique=True" in col_args:
        parts.append("unique")

    if "nullable=False" in col_args:
        parts.append("required")

    if "JSONB" in col_args:
        parts.append("stored as JSONB")

    if re.search(r'\bdefault\s*=\s*False\b', col_args):
        parts.append("default: `false`")

    if "onupdate" in col_args:
        parts.append("auto-set on update")
    elif re.search(r'\bdefault\s*=\s*datetime\b', col_args):
        parts.append("auto-set on creation")

    result = ", ".join(parts)
    return result[0].upper() + result[1:] if result else ""


def parse_models_file(file_path: str) -> list[dict]:
    """
    Parse a models.py file and return a list of model dicts, each with:
      - name  : class name
      - fields: list of (field_name, type_str, notes_str)
    """
    with open(file_path, encoding="utf-8") as fh:
        content = fh.read()

    enum_values = _parse_enum_values(content)

    model_re = re.compile(r'^class\s+(\w+)\s*\(\s*Base\s*\)\s*:', re.MULTILINE)
    models = []
    for model_match in model_re.finditer(content):
        class_name = model_match.group(1)
        class_start = model_match.end()
        next_class = re.search(r'^class\s+', content[class_start:], re.MULTILINE)
        class_body = (
            content[class_start: class_start + next_class.start()]
            if next_class
            else content[class_start:]
        )

        # Match: field_name: Mapped[type] = mapped_column(...)
        # Handles one level of bracket nesting in the type and one level of
        # parenthesis nesting in the column args (e.g. datetime.now(tz)).
        field_re = re.compile(
            r'^\s+(\w+)\s*:\s*Mapped\[([^\[\]]+(?:\[[^\[\]]*\])?)\]'
            r'\s*=\s*mapped_column\(([^()]*(?:\([^()]*\)[^()]*)*)\)',
            re.MULTILINE,
        )
        fields = []
        for field_name, mapped_type, col_args in field_re.findall(class_body):
            if field_name.startswith("_"):
                continue
            type_str = _parse_col_type(mapped_type, col_args, enum_values)
            notes = _parse_col_notes(col_args)
            fields.append((field_name, type_str, notes))

        if fields:
            models.append({"name": class_name, "fields": fields})

    return models


def find_models_files() -> list[str]:
    """Return paths to all models.py files under app/, sorted by directory name."""
    paths = []
    for dirpath, dirnames, filenames in os.walk(APP_DIR):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__")
        if "models.py" in filenames:
            paths.append(os.path.join(dirpath, "models.py"))
    return paths


def generate_models_section(model: dict) -> str:
    """Return a markdown table for one SQLAlchemy model."""
    lines = [
        f"### {model['name']}",
        "",
        "| Field | Type | Notes |",
        "|-------|------|-------|",
    ]
    for field_name, type_str, notes in model["fields"]:
        lines.append(f"| `{field_name}` | {type_str} | {notes} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# README update
# ---------------------------------------------------------------------------

def _replace_section(readme: str, start_marker: str, end_marker: str, new_content: str) -> str:
    """Replace the content between two markers and return the updated string."""
    start_idx = readme.find(start_marker)
    end_idx = readme.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print(f"WARNING: markers {start_marker!r} / {end_marker!r} not found in README.md – skipping.")
        return readme

    return (
        readme[: start_idx + len(start_marker)]
        + "\n\n"
        + new_content
        + "\n\n"
        + readme[end_idx:]
    )


def update_readme(sections: dict[tuple[str, str], str]) -> None:
    """
    Update README.md by replacing the content within each pair of markers.
    ``sections`` maps (start_marker, end_marker) → new_content.
    """
    with open(README_PATH, encoding="utf-8") as fh:
        readme = fh.read()

    for (start, end), content in sections.items():
        readme = _replace_section(readme, start, end, content)

    with open(README_PATH, "w", encoding="utf-8") as fh:
        fh.write(readme)

    print("README.md updated successfully.")


def main() -> None:
    sections: dict[tuple[str, str], str] = {}

    # --- API Endpoints ---
    router_files = get_router_modules()
    if router_files:
        router_sections = [generate_routers_section(parse_router_file(fp)) for fp in router_files]
        sections[(ROUTERS_START, ROUTERS_END)] = "\n\n".join(router_sections)
    else:
        print("No routers found in app/main.py – skipping API endpoints update.")

    # --- Project Structure ---
    sections[(PROJECT_STRUCTURE_START, PROJECT_STRUCTURE_END)] = generate_project_structure()

    # --- Data Models ---
    all_models = []
    for fp in find_models_files():
        all_models.extend(parse_models_file(fp))
    if all_models:
        sections[(DATA_MODELS_START, DATA_MODELS_END)] = "\n\n".join(
            generate_models_section(m) for m in all_models
        )
    else:
        print("No data models found – skipping data models update.")

    if sections:
        update_readme(sections)
    else:
        print("Nothing to update.")


if __name__ == "__main__":
    main()
