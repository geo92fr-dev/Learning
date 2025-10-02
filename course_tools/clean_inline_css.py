"""
Safely remove duplicated inline <style> blocks that contain specific selectors.
Creates a .bak backup for each modified file and writes a log at course_tools/clean_inline_css.log

Usage:
  python course_tools\clean_inline_css.py --root "c:\Project_Learning_Simplified"

This script looks for <style>...</style> blocks that contain any of the selectors in TARGET_SELECTORS
and removes only those <style> blocks. It leaves other <style> blocks intact.

Be conservative: if a <style> block contains one of the target selectors, the entire block is removed.
"""
import argparse
import os
import re
from datetime import datetime

TARGET_SELECTORS = [r".grid-auto", r".card", r".toggle", r".solution", r".badge", r".regle-box"]
STYLE_BLOCK_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.IGNORECASE | re.DOTALL)

LOG_PATH = os.path.join(os.path.dirname(__file__), "clean_inline_css.log")


def file_contains_target(style_block_text: str) -> bool:
    for sel in TARGET_SELECTORS:
        if re.search(re.escape(sel), style_block_text, re.IGNORECASE):
            return True
    return False


def process_file(path: str) -> bool:
    """Return True if modified"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = list(STYLE_BLOCK_RE.finditer(content))
    if not matches:
        return False

    to_remove_spans = []
    for m in matches:
        block = m.group(0)
        if file_contains_target(block):
            to_remove_spans.append((m.start(), m.end()))

    if not to_remove_spans:
        return False

    # Create backup
    bak_path = path + ".bak"
    if not os.path.exists(bak_path):
        with open(bak_path, "w", encoding="utf-8") as f:
            f.write(content)

    # Remove spans from the end to avoid shifting indexes
    new_content_parts = []
    last_idx = 0
    for start, end in to_remove_spans:
        new_content_parts.append(content[last_idx:start])
        last_idx = end
    new_content_parts.append(content[last_idx:])
    new_content = "".join(new_content_parts)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    with open(LOG_PATH, "a", encoding="utf-8") as logf:
        logf.write(f"{datetime.utcnow().isoformat()}Z REMOVED_STYLE_BLOCKS {path}\n")

    return True


def main(root: str):
    changed = []
    examined = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # skip .git and node_modules directories
        if ".git" in dirpath or "node_modules" in dirpath:
            continue
        for fn in filenames:
            if not fn.lower().endswith('.html'):
                continue
            path = os.path.join(dirpath, fn)
            examined += 1
            try:
                modified = process_file(path)
                if modified:
                    changed.append(path)
            except Exception as e:
                with open(LOG_PATH, "a", encoding="utf-8") as logf:
                    logf.write(f"{datetime.utcnow().isoformat()}Z ERROR {path} {e}\n")

    print(f"Examined {examined} HTML files. Modified {len(changed)} files. See {LOG_PATH} for details.")
    if changed:
        print("Modified files:")
        for p in changed:
            print(" - ", p)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', help='Root folder to scan', default='c:\\Project_Learning_Simplified')
    args = parser.parse_args()
    main(args.root)
