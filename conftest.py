import glob

import pytest


def _py_files(folder):
    return glob.glob(folder + "/*.py") + glob.glob(folder + "/*/*.py")


collect_ignore = [
    'convert_utils',
]

for line in open('tests/py3-ignores.txt'):
    file_path = line.strip()
    if file_path and file_path[0] != '#':
        collect_ignore.append(file_path)


@pytest.fixture()
def chdir(tmpdir):
    """Change to pytest-provided temporary directory"""
    tmpdir.chdir()
