#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from mesonui.repository.mesonapi import MesonAPI
from mesonui.mesonuilib.mesonapi.buildoptions import BuildOption
from mesonui.mesonuilib.mesonapi.projectinfo import ProjectInfo
from mesonui.mesonuilib.mesonapi.projectinfo import MesonInfo
from .backendimpl import BackendImplementionApi
from os.path import join as join_paths
from ..buildsystem import Meson
import logging
import os


class KDevelopBackend(BackendImplementionApi):
    def __init__(self, meson_api: MesonAPI):
        super(self.__class__, self).__init__(meson_api)
        self.backend: str = "'kdevelop'"
        self.buildoptions = BuildOption(meson_api=meson_api)
        self.projectinfo = ProjectInfo(meson_api=meson_api)
        self.mesoninfo = MesonInfo(meson_api=meson_api)
        self.meson = Meson()

    def generator(self):
        logging.info(f"Generating {self.backend} project")
        self.generate_project()

    def generate_project(self):
        # Generate the .kdev4 file.
        with open(
            join_paths(
                self.mesoninfo.builddir, f"{self.projectinfo.descriptive_name}.kdev4"
            ),
            "w",
        ) as file:
            file.write("[Project]\n")
            file.write("CreatedFrom=meson.build\n")
            file.write("Manager=KDevMesonManager\n")
            file.write(f"Name={self.projectinfo.descriptive_name}\n")

        # Make .kdev4/ directory.
        if not os.path.exists(join_paths(self.mesoninfo.builddir, ".kdev")):
            os.mkdir(join_paths(self.mesoninfo.builddir, ".kdev"))

        # Generate the .kdev4/ file.
        with open(
            join_paths(
                self.mesoninfo.builddir,
                ".kdev",
                f"{self.projectinfo.descriptive_name}.kdev4",
            ),
            "w",
        ) as file:
            file.write("[Buildset]\n")
            file.write(f"BuildItems=@Variant({self._variant()})\n\n")

            file.write("[MesonManager]\n")
            file.write("Current Build Directory Index=0\n")
            file.write("Number of Build Directories=1\n\n")

            file.write("[MesonManager][BuildDir 0]\n")
            file.write("Additional meson arguments=\n")
            file.write(f"Build Build Path={self.mesoninfo.builddir}\n")
            file.write(
                f'Meson Generator Backend={self.buildoptions.combo("backend").value}\n'
            )
            file.write(f"Meson executable={self.meson.exe}\n")

    def _variant(self) -> str:
        variant: str = (
            "\\x00\\x00\\x00\\t\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x0b\\x00\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x16"
        )
        for i in self.projectinfo.descriptive_name:
            variant + f"\\x00{i}"
        return variant
