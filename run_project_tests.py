#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
import pytest
from mesonui.mesonuilib.utilitylib import CIUtility
from mesonui.packageinfo import PackageInfo
from mesonui.projectinfo import ProjectInfo
from mesonui.authorinfo import ProjectAuthor
from mesonui.mesonuilib.buildsystem import Meson
from mesonui.mesonuilib.buildsystem import Ninja

from os.path import join as join_paths
import shutil
import os

TEST_WRAP: str = """\
[wrap-file]
directory = sqlite-amalgamation-3080802

source_url = http://sqlite.com/2015/sqlite-amalgamation-3080802.zip
source_filename = sqlite-amalgamation-3080802.zip
source_hash = 5ebeea0dfb75d090ea0e7ff84799b2a7a1550db3fe61eb5f6f61c2e971e57663

patch_url = https://wrapdb.mesonbuild.com/v1/projects/sqlite/3080802/5/get_zip
patch_filename = sqlite-3080802-5-wrap.zip
patch_hash = d66469a73fa1344562d56a1d7627d5d0ee4044a77b32d16cf4bbb85741d4c9fd
"""

info = """\
Meson-UI is an open source build GUI meant to be both extremely fast,
and, even more importantly, as user friendly as possible.

The main design point of Meson-UI is to provide a standalone portable
build GUI and allow the user to access all or most of Meson build
systems features.
"""


class TestPyPiPackageInfo:
    def test_all_pypi_info(self):
        pypi = PackageInfo()
        assert pypi.get_name() == "Michael Brockus"
        assert pypi.get_mail() == "michaelbrockus@gmail.com"
        assert pypi.get_license() == "Apache-2.0"
        assert pypi.get_project_name() == "meson-ui"
        assert pypi.get_version() == "0.20.1"
        assert pypi.get_description() == info

    def test_only_author_info(self):
        pypi = ProjectAuthor()
        assert pypi.get_name() == "Michael Brockus"
        assert pypi.get_mail() == "michaelbrockus@gmail.com"

    def test_only_project_info(self):
        pypi = ProjectInfo()
        assert pypi.get_license() == "Apache-2.0"
        assert pypi.get_project_name() == "meson-ui"
        assert pypi.get_version() == "0.20.1"
        assert pypi.get_description() == info


class TestNinja:

    def test_change_sourcedir(self):
        ninja = Ninja("test/dir/one", "test/dir/one/builddir")

        assert ninja.sourcedir == "test/dir/one"
        assert ninja.builddir == "test/dir/one/builddir"

        ninja.sourcedir = "test/dir/two"
        ninja.builddir = "test/dir/two/builddir"

        assert ninja.sourcedir == "test/dir/two"
        assert ninja.builddir == "test/dir/two/builddir"

    def test_build_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        ninja: Ninja = Ninja(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])
        ninja.build()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    def test_clean_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        ninja: Ninja = Ninja(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])
        ninja.build()
        ninja.clean()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    def test_ninja_test_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        ninja: Ninja = Ninja(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])
        ninja.build()
        ninja.test()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()


class TestMeson:

    def test_change_sourcedir(self):
        meson = Meson("test/dir/one", "test/dir/one/builddir")

        assert meson.sourcedir == "test/dir/one"
        assert meson.builddir == "test/dir/one/builddir"

        meson.sourcedir = "test/dir/two"
        meson.builddir = "test/dir/two/builddir"

        assert meson.sourcedir == "test/dir/two"
        assert meson.builddir == "test/dir/two/builddir"

    def test_setup_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    def test_build_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])
        meson.build()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    def test_configure_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])
        meson.configure(["--werror", "--buildtype=minsize"])

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    def test_rebuild_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])
        meson.compile()

        meson.setup(["--wipe"])

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    def test_compile_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])
        meson.compile()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    def test_clean_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])
        meson.compile()
        meson.clean()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    def test_install_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])
        meson.compile()
        meson.install()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    def test_mtest_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])
        meson.compile()
        meson.test()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    @pytest.mark.skipif(
        not shutil.which("git"), reason='Did not find "git" on this system'
    )
    def test_mdist_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c", "--type=executable"])
        meson.setup(["--backend=ninja"])
        meson.compile()

        CIUtility._git_init()
        meson.dist()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()
        assert tmpdir.join(
            "builddir", "meson-dist", "test_mdist_command0-0.1.tar.xz"
        ).ensure()

    def test_init_command(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))

        meson.init(["--language=c"])
        meson.setup()
        meson.compile()
        meson.test()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    @pytest.mark.skipif(
        not shutil.which("git"), reason='Did not find "git" on this system'
    )
    def test_subproject_checkout_subcommand(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        meson.init(["--language=c", "--deps", "samplesubproject"])
        os.mkdir("subprojects")

        tmpdir.join(join_paths("subprojects", "samplesubproject.wrap")).write(
            """\
        [wrap-git]
        directory=samplesubproject
        url=https://github.com/jpakkane/samplesubproject.git
        revision=head
        """
        )

        meson.subprojects().download("samplesubproject")
        meson.subprojects().checkout("master", "samplesubproject")

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("subprojects", "samplesubproject.wrap").ensure()
        assert tmpdir.join("subprojects", "samplesubproject", ".gitignore").ensure()
        assert tmpdir.join("subprojects", "samplesubproject", "README.md").ensure()

    def test_subproject_update_subcommand(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        meson.init(["--language=c", "--deps", "sqlite"])
        os.mkdir("subprojects")

        tmpdir.join(join_paths("subprojects", "sqlite.wrap")).write(TEST_WRAP)

        meson.subprojects().download("sqlite")
        meson.subprojects().update("sqlite")

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("subprojects", "sqlite.wrap").ensure()

    def test_subproject_download_subcommand(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        meson.init(["--language=c", "--deps", "sqlite"])
        os.mkdir("subprojects")

        tmpdir.join(join_paths("subprojects", "sqlite.wrap")).write(TEST_WRAP)

        meson.subprojects().download("sqlite")

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("subprojects", "sqlite.wrap").ensure()

    def test_wrap_info_subcommand(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        meson.init(["--language=c", "--deps", "sqlite"])
        os.mkdir("subprojects")

        tmpdir.join(join_paths("subprojects", "sqlite.wrap")).write(TEST_WRAP)

        meson.wrap().info("sqlite")

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("subprojects", "sqlite.wrap").ensure()

    def test_wrap_search_subcommand(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        meson.init(["--language=c", "--deps", "sqlite"])
        os.mkdir("subprojects")

        tmpdir.join(join_paths("subprojects", "sqlite.wrap")).write(TEST_WRAP)

        meson.wrap().search("sqlite")

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("subprojects", "sqlite.wrap").ensure()

    def test_wrap_install_subcommand(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        meson.init(["--language=c", "--deps", "sqlite"])
        os.mkdir("subprojects")

        meson.wrap().install("sqlite")

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("subprojects", "sqlite.wrap").ensure()

    def test_wrap_status_subcommand(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        meson.init(["--language=c", "--deps", "sqlite"])
        os.mkdir("subprojects")

        tmpdir.join(join_paths("subprojects", "sqlite.wrap")).write(TEST_WRAP)

        meson.wrap().status()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("subprojects", "sqlite.wrap").ensure()

    def test_wrap_update_subcommand(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        meson.init(["--language=c", "--deps", "sqlite"])
        os.mkdir("subprojects")

        tmpdir.join(join_paths("subprojects", "sqlite.wrap")).write(TEST_WRAP)

        meson.wrap().update("sqlite")

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("subprojects", "sqlite.wrap").ensure()

    def test_wrap_list_subcommand(self, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        #
        # Running Meson command
        meson: Meson = Meson(sourcedir=tmpdir, builddir=(tmpdir / "builddir"))
        meson.init(["--language=c", "--deps", "sqlite"])
        os.mkdir("subprojects")

        tmpdir.join(join_paths("subprojects", "sqlite.wrap")).write(TEST_WRAP)

        meson.wrap().list_wraps()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("subprojects", "sqlite.wrap").ensure()
