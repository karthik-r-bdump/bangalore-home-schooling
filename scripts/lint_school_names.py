#!/usr/bin/env python3
"""
Redaction Linter for Bangalore Home Schooling
Ensures no specific school names or identifying references exist in docs, static, or code.
"""

import os
import sys
import re

FORBIDDEN_PATTERNS = [
    (re.compile(r'\bFAPS\b', re.IGNORECASE), "FAPS (The Frank Anthony Public School)"),
    (re.compile(r'Frank\s+Anthony', re.IGNORECASE), "The Frank Anthony Public School"),
    (re.compile(r'Bishop\s+Cotton', re.IGNORECASE), "Bishop Cotton School"),
    (re.compile(r'Greenwood\s+High', re.IGNORECASE), "Greenwood High"),
    (re.compile(r'Delhi\s+Public\s+School', re.IGNORECASE), "Delhi Public School"),
    (re.compile(r'National\s+Public\s+School', re.IGNORECASE), "National Public School"),
]

# File extensions to check content
TEXT_EXTENSIONS = {'.md', '.mdx', '.txt', '.ts', '.tsx', '.js', '.jsx', '.json', '.css', '.html', '.yml', '.yaml'}

# Directories to scan
SCAN_DIRS = ['docs', 'src', 'static']
SCAN_ROOT_FILES = ['docusaurus.config.ts', 'sidebars.ts', 'README.md', 'CONTRIBUTING.md']

# Directories to ignore
IGNORE_DIRS = {'node_modules', '.git', 'build', '.docusaurus', 'scripts', '.agents'}

def check_file_name(rel_path):
    violations = []
    basename = os.path.basename(rel_path)
    for pattern, desc in FORBIDDEN_PATTERNS:
        if pattern.search(basename):
            violations.append((rel_path, 0, f"File name contains forbidden reference: {desc}"))
    return violations

def check_file_content(filepath, rel_path):
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern, desc in FORBIDDEN_PATTERNS:
                    if pattern.search(line):
                        violations.append((rel_path, line_num, line.strip(), desc))
    except Exception as e:
        print(f"Warning: Could not read {rel_path}: {e}", file=sys.stderr)
    return violations

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    all_violations = []

    print("🔍 Running School-Agnostic Redaction Linter...")

    # Check designated directories
    for scan_dir in SCAN_DIRS:
        dir_path = os.path.join(root_dir, scan_dir)
        if not os.path.exists(dir_path):
            continue
        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, root_dir)
                
                # Check filename
                fn_violations = check_file_name(rel_path)
                all_violations.extend(fn_violations)

                # Check content for text files
                ext = os.path.splitext(file)[1].lower()
                if ext in TEXT_EXTENSIONS:
                    c_violations = check_file_content(filepath, rel_path)
                    all_violations.extend(c_violations)

    # Check root files
    for rf in SCAN_ROOT_FILES:
        rf_path = os.path.join(root_dir, rf)
        if os.path.exists(rf_path):
            c_violations = check_file_content(rf_path, rf)
            all_violations.extend(c_violations)

    if all_violations:
        print(f"\n❌ Redaction Lint Failed! Found {len(all_violations)} violation(s):\n", file=sys.stderr)
        for v in all_violations:
            if len(v) == 3:
                rel_path, line_num, msg = v
                print(f"  • {rel_path}: {msg}", file=sys.stderr)
            else:
                rel_path, line_num, line_txt, desc = v
                print(f"  • {rel_path}:{line_num} [{desc}] -> \"{line_txt}\"", file=sys.stderr)
        print("\n🚫 Please remove or sanitize all school-specific references before committing.", file=sys.stderr)
        sys.exit(1)
    else:
        print("✅ Redaction Lint Passed! Zero school-specific references found.")
        sys.exit(0)

if __name__ == '__main__':
    main()
