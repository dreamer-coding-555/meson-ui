#!/usr/bin/env python3
#
# Trilobite AppHub:
# author: Michael Gene Brockus (Dreamer)
# Gmail: <mail: michaelbrockus@gmail.com>
#
from code.main import main_prog
from pathlib import Path
import sys

# If we run uninstalled, add the script directory to sys.path to ensure that
# we always import the correct program modules even if PYTHON_PATH is mangled
exe = Path(sys.argv[0]).resolve()
if (exe.parent / 'prog').is_dir():
    sys.path.insert(0, str(exe.parent))

if __name__ == "__main__":
    sys.exit(main_prog())
