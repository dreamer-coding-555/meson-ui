#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from mesonui.mesonuilib.xmlbuilder import Builder
from mesonui.repository.mesonapi import MesonAPI
from mesonui.mesonuilib.mesonapi.projectinfo import ProjectInfo
from mesonui.mesonuilib.mesonapi.projectinfo import MesonInfo
from .backendimpl import BackendImplementionApi
from os.path import join as join_paths
from ..buildsystem import Ninja
import logging
import os

BUILD_OPTION_EXECUTABLE = 1
BUILD_OPTION_STATIC_LIBRARY = 2
BUILD_OPTION_SHARED_LIBRARY = 3
BUILD_OPTION_COMMANDS_ONLY = 4
CBP_VERSION_MAJOR = 1
CBP_VERSION_MINOR = 6


class CodeBlocksBackend(BackendImplementionApi):
    def __init__(self, meson_api: MesonAPI):
        self.backend: str = "'codeblocks'"
        self.projectinfo = ProjectInfo(meson_api=meson_api)
        self.mesoninfo = MesonInfo(meson_api=meson_api)
        self.buildsystem_files = meson_api.get_object(
            group="buildsystem-files", extract_method="loader"
        )
        self.targetsinfo: any = meson_api.get_object(
            group="targets", extract_method="loader"
        )
        self.ninja = Ninja(self.mesoninfo.sourcedir, self.mesoninfo.builddir)
        self.compiler = self.targetsinfo[0]["target_sources"][0]["compiler"][0]

    def generator(self):
        logging.info(f"Generating {self.backend} project")
        self.generate_project()

    def generate_project(self):
        xml: Builder = Builder(version="1.0", encoding="UTF-8")
        with xml.CodeBlocks_project_file(
            Name=self.projectinfo.descriptive_name,
            Version="0.1",
            InternalType="Console",
        ):
            xml.FileVersion(major=f"{CBP_VERSION_MAJOR}", minor=f"{CBP_VERSION_MINOR}")
            with xml.Project:
                xml.Option(title=self.projectinfo.descriptive_name)
                xml.Option(compiler=self.compiler)
                xml.Option(virtualFolders="Meson Files")
                xml.Option(makefile_is_custom="1")

            with xml.Build:
                for targets in self.targetsinfo:
                    output = join_paths(self.mesoninfo.builddir, targets["id"])
                    with xml.Target(title=targets["name"]):
                        xml.Option(output=output)
                        xml.Option(working_dir=os.path.split(output)[0])
                        xml.Option(
                            object_output=join_paths(
                                os.path.split(output)[0], targets["id"]
                            )
                        )
                        ty = {
                            "executable": f"{BUILD_OPTION_EXECUTABLE}",
                            "static library": f"{BUILD_OPTION_STATIC_LIBRARY}",
                            "shared library": f"{BUILD_OPTION_SHARED_LIBRARY}",
                            "custom": f"{BUILD_OPTION_COMMANDS_ONLY}",
                            "run": f"{BUILD_OPTION_COMMANDS_ONLY}",
                        }[targets["type"]]
                        xml.Option(type=ty)
                        compiler = targets
                        if compiler:
                            xml.Option(compiler=self.compiler)
                    with xml.Compiler:
                        for target in targets["target_sources"]:
                            for defs in target["parameters"]:
                                if defs.startswith("-D"):
                                    logging.info(f"add def: {defs}")
                                    xml.Add(option=defs)

                            for dirs in target["parameters"]:
                                if dirs.startswith("-I") or dirs.startswith("/I"):
                                    logging.info(f"add include: {dirs}")
                                    xml.Add(option=dirs)

                    with xml.MakeCommands:
                        xml.Build(command=f'{self.ninja.exe} -v {targets["name"]}')
                        xml.CompileFile(
                            command=f'{self.ninja.exe} -v {targets["name"]}'
                        )
                        xml.Clean(command=f"{self.ninja.exe} -v clean")
                        xml.DistClean(command=f"{self.ninja.exe} -v clean")

            for targets in self.targetsinfo:
                for target in targets["target_sources"]:
                    for file in target["sources"]:
                        with xml.Unit(
                            filename=join_paths(self.mesoninfo.sourcedir, file)
                        ):
                            xml.Option(target=targets["name"])

                    base = os.path.splitext(os.path.basename(file))[0]
                    header_exts = ("h", "hpp")
                    for ext in header_exts:
                        header_file = os.path.abspath(
                            join_paths(
                                self.mesoninfo.sourcedir,
                                os.path.dirname(file),
                                f"{base}.{ext}",
                            )
                        )
                        if os.path.exists(header_file):
                            with xml.Unit(filename=header_file):
                                xml.Option(target=targets["name"])
            for file in self.buildsystem_files:
                with xml.Unit(filename=join_paths(self.mesoninfo.sourcedir, file)):
                    xml.Option(target=join_paths("Meson Files", os.path.dirname(file)))

        with open(
            join_paths(
                self.mesoninfo.builddir, f"{self.projectinfo.descriptive_name}.cbp"
            ),
            "w",
        ) as ide_file:
            ide_file.write(str(xml))
