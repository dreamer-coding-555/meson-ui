#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from mesonui.repository.mesonapi import MesonAPI
from mesonui.mesonuilib.mesonapi.projectinfo import ProjectInfo
from mesonui.mesonuilib.mesonapi.projectinfo import MesonInfo
from .backendimpl import BackendImplementionApi
from os.path import join as join_paths
import logging
import os


class QtCreatorBackend(BackendImplementionApi):
    def __init__(self, meson_api: MesonAPI):
        self.backend: str = "'qtcreator'"
        self.projectinfo = ProjectInfo(meson_api=meson_api)
        self.mesoninfo = MesonInfo(meson_api=meson_api)
        self.buildsystem_files: list = meson_api.get_object(
            group="buildsystem-files", extract_method="loader"
        )
        self.targetsinfo: list = meson_api.get_object(
            group="targets", extract_method="loader"
        )

    def generator(self):
        logging.info(f"Generating {self.backend} project")
        self.generate_project()

    def generate_project(self):
        # Generate the .creator file.
        with open(
            join_paths(
                self.mesoninfo.builddir, f"{self.projectinfo.descriptive_name}.creator"
            ),
            "w",
        ) as file:
            file.write("[General]")

        # Generate the .config file.
        with open(
            join_paths(
                self.mesoninfo.builddir, f"{self.projectinfo.descriptive_name}.config"
            ),
            "w",
        ) as file:
            file.write("// Add predefined macros for your project here. For example:")
            file.write("// #define THE_ANSWER 42")
            for targets in self.targetsinfo:
                for item in targets["target_sources"][0]["parameters"]:
                    if item.startswith("-D"):
                        logging.info(f"add def: {item}")
                        item = " ".join(item.split("="))
                        file.write(f"#define {item}\n")

        # Generate the .files file.
        with open(
            join_paths(
                self.mesoninfo.builddir, f"{self.projectinfo.descriptive_name}.files"
            ),
            "w",
        ) as file:
            for targets in self.targetsinfo:
                for items in targets["target_sources"][0]["sources"]:
                    file.write(os.path.relpath(item, self.mesoninfo.builddir) + "\n")

                for item in self.buildsystem_files:
                    file.write(os.path.relpath(item, self.mesoninfo.builddir) + "\n")

        # Generate the .includes file.
        with open(
            join_paths(
                self.mesoninfo.builddir, f"{self.projectinfo.descriptive_name}.includes"
            ),
            "w",
        ) as file:
            for targets in self.targetsinfo:
                for item in targets["target_sources"][0]["parameters"]:
                    if item.startswith("-I") or item.startswith("/I"):
                        file.write(
                            os.path.relpath(item, self.mesoninfo.builddir) + "\n"
                        )
