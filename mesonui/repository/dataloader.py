#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from os.path import join as join_paths
from pathlib import Path
import logging
import json

_MESON_INTRO_FILES: tuple = (
    "intro-benchmarks.json",
    "intro-buildoptions.json",
    "intro-buildsystem_files.json",
    "intro-dependencies.json",
    "intro-installed.json",
    "intro-projectinfo.json",
    "intro-targets.json",
    "intro-tests.json",
    "meson-info.json",
)


class MesonBuilddirLoader:
    def __init__(self, builddir: Path = None):
        self._builddir = builddir

    def _scan(self, group: str) -> any:
        if group == "testlog.json":
            subdir = "meson-logs"
            if not Path(join_paths(self._builddir, subdir, group)).exists():
                return None
        else:
            subdir = "meson-info"
        with open(join_paths(self._builddir, subdir, group)) as loaded_json:
            info: any = json.loads(loaded_json.read())
        return info

    def extract_from(self, group: str):
        logging.info(f"Try getting {group} API object via build directory loader")
        if group == "buildoptions":
            return self._scan(group=f"intro-{group}.json")
        elif group == "meson-info":
            return self._scan(group=f"{group}.json")
        elif group == "testlog":
            return self._scan(group=f"{group}.json")
        elif group == "tests":
            return self._scan(group=f"intro-{group}.json")
        elif group == "benchmarks":
            return self._scan(group=f"intro-{group}.json")
        elif group == "buildsystem-files":
            return self._scan(group="intro-buildsystem_files.json")
        elif group == "projectinfo":
            return self._scan(group=f"intro-{group}.json")
        elif group == "dependencies":
            return self._scan(group=f"intro-{group}.json")
        elif group == "installed":
            return self._scan(group=f"intro-{group}.json")
        elif group == "targets":
            return self._scan(group=f"intro-{group}.json")
        else:
            raise Exception(f"Group tag {group} not found in extract via data options!")
