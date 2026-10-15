#!/usr/bin/env python3
"""Inspect local marketplace packages or an installed plugin/skill directory."""
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_file(root, path):
    target = (root / path).resolve()
    require(target.is_relative_to(root.resolve()), f"Path escapes package: {path}")
    require(target.is_file(), f"Missing package file: {path}")
    return target


def inventory(root):
    entries = sorted(root.rglob("*"))
    require(not any(p.is_symlink() for p in entries), f"Review symlinks in {root}")
    files = [p for p in entries if p.is_file()]
    for p in files:
        relative = p.relative_to(root)
        require(not any(part in {".git", "__pycache__", ".DS_Store", "tests"}
                        for part in relative.parts), f"Development artifact: {relative}")
    return files


def check_markdown(root):
    # Check actual local Markdown/HTML targets, excluding fenced command examples.
    for p in root.rglob("*.md"):
        body = re.sub(r"```.*?```", "", p.read_text(), flags=re.S)
        targets = re.findall(r'!?\[[^\]]*\]\(([^)]+)\)|(?:src|href)="([^"]+)"', body)
        for markdown, html in targets:
            target = (markdown or html).split(' "', 1)[0].strip("<>")
            url = urlsplit(target)
            if not url.scheme and not url.netloc and url.path:
                path = (p.parent / unquote(url.path)).resolve()
                require(path.is_relative_to(root.resolve()), f"Link leaves package: {p}: {target}")
                require(path.exists(), f"Broken link: {p}: {target}")


def check_skill(root):
    files = inventory(root)
    local_file(root, "SKILL.md")
    local_file(root, "LICENSE")
    allowed = {"SKILL.md", "LICENSE", "PROTOCOL.md", "STYLES.md", "agents", "assets", "references", "scripts"}
    require(all(p.name in allowed for p in root.iterdir()), f"Unexpected skill-root content: {root}")
    check_markdown(root)
    print(f"Skill {root.name}: {len(files)} files; local links stay inside the skill")


def check_plugin(root):
    files = inventory(root)
    manifest = json.loads(local_file(root, ".codex-plugin/plugin.json").read_text())
    local_file(root, "LICENSE")
    require(all(p.name in {".codex-plugin", "skills", "assets", "LICENSE"}
                for p in root.iterdir()), f"Repository material at plugin root: {root}")
    skills = (root / manifest["skills"]).resolve()
    require(skills.is_relative_to(root.resolve()), f"Skills path leaves {root}")
    for skill in sorted(skills.iterdir()):
        if skill.is_dir():
            check_skill(skill)
    interface = manifest.get("interface", {})
    image_paths = interface.get("screenshots", []) + [
        interface[key] for key in ("iconSmall", "iconLarge") if interface.get(key)
    ]
    declared_images = {local_file(root, path) for path in image_paths}
    # Plugin-level images are UI resources. Generation references live in the skills.
    for p in (root / "assets").rglob("*"):
        if p.is_file():
            require(p.resolve() in declared_images, f"Undeclared plugin UI asset: {p}")
    print(f"Plugin {manifest['name']} {manifest['version']}: {len(files)} files; {len(declared_images)} declared UI images")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin", type=Path, help="Check one actual plugin installation directory")
    parser.add_argument("--skill", type=Path, help="Check one actual standalone skill installation directory")
    args = parser.parse_args()
    if args.plugin:
        check_plugin(args.plugin.resolve())
    elif args.skill:
        check_skill(args.skill.resolve())
    else:
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        for plugin in marketplace["plugins"]:
            source = plugin["source"]
            require(source["source"] == "local", f"Review non-local source: {source}")
            root = (ROOT / source["path"]).resolve()
            require(root.is_relative_to(ROOT), f"Marketplace source escapes repository: {source}")
            check_plugin(root)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print(f"Package check failed: {error}", file=sys.stderr)
        sys.exit(1)
