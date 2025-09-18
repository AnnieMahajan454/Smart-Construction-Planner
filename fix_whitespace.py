#!/usr/bin/env python3
"""Script to fix whitespace issues in all Python files."""
import os
import re
import glob

def fix_file_whitespace(file_path):
    """Fix trailing whitespace and blank line issues in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Fix trailing whitespace and blank lines containing whitespace
        fixed_lines = []
        for line in lines:
            # Remove trailing whitespace
            fixed_line = line.rstrip() + '\n'
            # If the line is now just '\n', it's a proper blank line
            fixed_lines.append(fixed_line)

        # Remove the final newline if the last line is empty to avoid extra newline
        if fixed_lines and fixed_lines[-1] == '\n':
            fixed_lines[-1] = fixed_lines[-1].rstrip()

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)

        print(f"Fixed: {file_path}")
        return True

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Fix whitespace issues in all Python files."""
    # Find all Python files recursively
    python_files = []
    for pattern in ['*.py', '*/*.py', '*/*/*.py']:
        python_files.extend(glob.glob(pattern))

    print(f"Found {len(python_files)} Python files to fix:")

    success_count = 0
    for file_path in python_files:
        if fix_file_whitespace(file_path):
            success_count += 1

    print(f"\nFixed {success_count} out of {len(python_files)} files.")

if __name__ == '__main__':
    main()
