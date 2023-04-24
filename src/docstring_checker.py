# cmd: git diff --cached --name-only

import re
import subprocess
from pathlib import Path
from pathlib import PurePath
from typing import List

GIT_DIFF_CMD = 'git diff --cached --name-only'
GIT_CI_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT_DIR = GIT_CI_DIR.parent.resolve()

whitelist_functions = ['main']

re_with_docstring = r'def\s(\S+|_\S+)((\(.?|[\S\s]+\))).+:((\n)|(\r\n))[ \t]+\"{3}[^\"]+\"{3}$'
re_without_docstring = r'def\s(\S+|\_S+)((\(.?|[\S\s]+\))).+:'

def get_commit_py() -> list:
    """Gets commit python file."""
    check_py_list = []
    result = subprocess.run(GIT_DIFF_CMD.split(' '), stdout=subprocess.PIPE)
    stdout = result.stdout.decode('utf-8')
    for f in stdout.split("\n"):
        fp = PurePath.joinpath(PROJECT_ROOT_DIR, f)
        if fp.suffix:
            if fp.suffix == ".py":
                check_py_list.append(fp)
    return check_py_list

def check_doc_string(fp_list: List[PurePath]):
    """Checks function that contains docstring."""
    for fp in fp_list:
        with open(fp, 'r') as pyf:
            data = pyf.readlines()
            for index, line in enumerate(data):
                if line.startswith('def'):
                    if not any(x in line for x in whitelist_functions):
                        check_line = line + data[index + 1]
                        functions_with_docstring = re.match(re_with_docstring, check_line)
                        if not functions_with_docstring:
                            no_docstring = re.match(re_without_docstring, check_line)
                            if no_docstring:
                                print(f"functions that don't have docstring `{no_docstring.group(1)}`")
                                return 1
    return 0


def main():
    commit_file_list = get_commit_py()
    return check_doc_string(commit_file_list)


if __name__ == "__main__":
    raise SystemExit(main())