from __future__ import annotations

import os
import subprocess
from pathlib import Path
from pathlib import PurePath

TESTING_DIR = Path(__file__).resolve().parent

def get_resource_path(path: PurePath):
    return PurePath.joinpath(TESTING_DIR, 'resoureces', path) 

def git_commit(*args, **kwargs):
    cmd = ('git', 'commit', '--no-gpg-sign', '--no-verify', '--no-edit', *args)
    subprocess.check_call(cmd, **kwargs)
