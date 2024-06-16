#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from subprocess import check_call
from subprocess import STDOUT


cmd: list = [
    "pytest",
    "-v",
    "--cov=./",
    "run_unittests.py",
    "run_backend_tests.py",
    "run_project_tests.py",
    "run_mesonui_tests.py",
]

check_call(cmd, encoding="utf8", stderr=STDOUT)
