#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
import pytest
from mesonui.mesonuilib.utilitylib import OSUtility
from mesonui.mesonuilib.buildsystem import Meson
from mesonui.mesonuilib.backends.qtcreator import QtCreatorBackend
from mesonui.mesonuilib.backends.kdevelop import KDevelopBackend
from mesonui.mesonuilib.backends.gnome import GNOMEBuilderBackend

from mesonui.repository.mesonapi import MesonAPI
from os.path import join as join_paths
from pathlib import Path
import os


class TestMesonBackend:

    def test_kdevelop_backend(self):
        #
        # Setting up tmp test directory
        source = Path(join_paths("test-cases", "backends", "01-kdevelop")).resolve()
        build = Path(
            join_paths("test-cases", "backends", "01-kdevelop", "builddir")
        ).resolve()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup(["--backend=ninja"])
        api = MesonAPI(sourcedir=source, builddir=build)
        ide = KDevelopBackend(api)
        ide.generator()

        #
        # Run asserts to check it is working
        assert os.path.exists(join_paths(source, "meson.build"))
        assert os.path.exists(join_paths(build, "build.ninja"))
        assert os.path.exists(join_paths(build, "meson-info", "intro-projectinfo.json"))
        assert os.path.exists(join_paths(build, "compile_commands.json"))
        assert os.path.exists(join_paths(build, "basic.kdev4"))

    def test_qtcreator_backend(self):
        #
        # Setting up tmp test directory
        source = Path(join_paths("test-cases", "backends", "03-qtcreator"))
        build = Path(join_paths("test-cases", "backends", "03-qtcreator", "builddir"))

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()
        api = MesonAPI(sourcedir=source, builddir=build)
        ide = QtCreatorBackend(api)
        ide.generator()

        #
        # Run asserts to check it is working
        assert os.path.exists(join_paths(source, "meson.build"))
        assert os.path.exists(join_paths(build, "build.ninja"))
        assert os.path.exists(join_paths(build, "meson-info", "intro-projectinfo.json"))
        assert os.path.exists(join_paths(build, "compile_commands.json"))
        assert os.path.exists(join_paths(build, "basic.creator"))
        assert os.path.exists(join_paths(build, "basic.includes"))
        assert os.path.exists(join_paths(build, "basic.files"))

    def test_gnome_builder_backend(self):
        #
        # Setting up tmp test directory
        source = Path(join_paths("test-cases", "backends", "04-gnome")).resolve()
        build = Path(
            join_paths("test-cases", "backends", "04-gnome", "builddir")
        ).resolve()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup(["--backend=ninja"])
        api = MesonAPI(sourcedir=source, builddir=build)
        ide = GNOMEBuilderBackend(api)
        ide.generator()

        #
        # Run asserts to check it is working
        assert os.path.exists(join_paths(source, "meson.build"))
        assert os.path.exists(join_paths(build, "build.ninja"))
        assert os.path.exists(join_paths(build, "compile_commands.json"))

    def test_ninja_backend(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c"])
        meson.setup(["--backend=ninja"])

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    @pytest.mark.skipif(
        not OSUtility.is_osx(),
        reason="Skipping because Xcode backend only works on OSX systems",
    )
    def test_xcode_backend(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=xcode"])
        meson.compile()
        meson.test()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()
        assert tmpdir.join(
            "builddir", "test-prog.xcodeproj", "project.pbxproj"
        ).ensure()

    @pytest.mark.skipif(
        not OSUtility.is_windows(),
        reason="Skipping because Visual Studio backend only works on Windows",
    )
    def test_vs_backend(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c"])
        meson.setup(["--backend=vs"])

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()


# TestMesonBackend().test_codeblocks_backend()
