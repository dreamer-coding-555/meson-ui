#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from mesonui.view.main_activity import MainActivity
from mesonui.view.setup_activity import SetupActivity
from mesonui.view.conf_activity import ConfigureActivity
from mesonui.view.dist_activity import DistActivity
from mesonui.view.init_activity import InitActivity
from mesonui.view.wrap_activity import WrapActivity
from mesonui.view.install_activity import InstallActivity
from mesonui.view.subprojects_activity import SubprojectsActivity
from mesonui.mesonuilib.outputconsole import OutputConsole

from mesonui.models.appmodel import MainModel
from PyQt5.QtCore import Qt


class TestMainActivity:
    def test_is_renderable(self, qtbot):
        activity = MainActivity(MainModel())
        qtbot.addWidget(activity)

    def test_enter_values(self, qtbot, tmpdir):
        activity = MainActivity(MainModel())
        qtbot.addWidget(activity)

        activity.project_sourcedir.clear()
        qtbot.keyClicks(activity.project_sourcedir, str(tmpdir))

        activity.project_builddir.clear()
        qtbot.keyClicks(activity.project_builddir, str((tmpdir / "builddir")))

        assert activity.project_sourcedir.text() == str(tmpdir)
        assert activity.project_builddir.text() == str(tmpdir / "builddir")

    def test_enter_clear(self, qtbot, tmpdir):
        activity = MainActivity(MainModel())
        qtbot.addWidget(activity)

        activity.project_sourcedir.clear()
        qtbot.keyClicks(activity.project_sourcedir, str(tmpdir))

        activity.project_builddir.clear()
        qtbot.keyClicks(activity.project_builddir, str((tmpdir / "builddir")))

        assert activity.project_sourcedir.text() == str(tmpdir)
        assert activity.project_builddir.text() == str(tmpdir / "builddir")

        qtbot.mouseClick(activity.control_push_clear_sourcedir, Qt.LeftButton)

        assert activity.project_sourcedir.text() == ""
        assert activity.project_builddir.text() == ""


class TestSetupActivity:
    def test_is_renderable(self, qtbot):
        activity = SetupActivity(None, MainModel())
        qtbot.addWidget(activity)

    def test_do_setup_prog(self, qtbot, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        model = MainModel()
        model.buildsystem().meson().sourcedir = tmpdir
        model.buildsystem().meson().builddir = tmpdir / "builddir"
        model.buildsystem().meson().init()

        setup_view: SetupActivity = SetupActivity(
            OutputConsole(MainActivity(model)), model
        )
        qtbot.addWidget(setup_view)

        qtbot.mouseClick(setup_view.control_push_do_setup, Qt.LeftButton)
        model.buildsystem().meson().compile()
        model.buildsystem().meson().test()

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    def test_no_setup_prog(self, qtbot):
        setup_view: SetupActivity = SetupActivity(None, MainModel())
        qtbot.addWidget(setup_view)

        qtbot.mouseClick(setup_view.control_push_no_setup, Qt.LeftButton)


class TestConfigureActivity:
    def test_is_renderable(self, qtbot):
        activity = ConfigureActivity(None, MainModel())
        qtbot.addWidget(activity)

    def test_do_configure_prog(self, qtbot, tmpdir):
        #
        # Setting up tmp test directory
        with tmpdir.as_cwd():
            pass
        tmpdir.chdir()

        model = MainModel()
        model.buildsystem().meson().sourcedir = tmpdir
        model.buildsystem().meson().builddir = tmpdir / "builddir"
        model.buildsystem().meson().init()

        setup_view: ConfigureActivity = ConfigureActivity(
            OutputConsole(MainActivity(MainModel())), model
        )
        qtbot.addWidget(setup_view)

        qtbot.mouseClick(setup_view.control_push_do_setup, Qt.LeftButton)

        #
        # Run asserts to check it is working
        assert tmpdir.join("meson.build").ensure()
        assert tmpdir.join("builddir", "build.ninja").ensure()
        assert tmpdir.join("builddir", "compile_commands.json").ensure()

    def test_no_setup_prog(self, qtbot):
        setup_view: ConfigureActivity = ConfigureActivity(None, MainModel())
        qtbot.addWidget(setup_view)

        qtbot.mouseClick(setup_view.control_push_no_setup, Qt.LeftButton)


class TestInitActivity:
    def test_is_renderable(self, qtbot):
        activity = InitActivity(MainModel())
        qtbot.addWidget(activity)

    def test_no_init_prog(self, qtbot):
        setup_view: InitActivity = InitActivity(MainModel())
        qtbot.addWidget(setup_view)

        qtbot.mouseClick(setup_view.control_push_no_init, Qt.LeftButton)


class TestDistActivity:
    def test_is_renderable(self, qtbot):
        activity = DistActivity(MainModel())
        qtbot.addWidget(activity)

    def test_no_dist_prog(self, qtbot):
        setup_view: DistActivity = DistActivity(MainModel())
        qtbot.addWidget(setup_view)

        qtbot.mouseClick(setup_view.control_push_no_dist, Qt.LeftButton)


class TestWrapActivity:
    def test_is_renderable(self, qtbot):
        activity = WrapActivity(MainModel())
        qtbot.addWidget(activity)

    def test_exit_wraptools(self, qtbot):
        setup_view: WrapActivity = WrapActivity(MainModel())
        qtbot.addWidget(setup_view)

        qtbot.mouseClick(setup_view.control_push_ok, Qt.LeftButton)


class TestInstallActivity:
    def test_is_renderable(self, qtbot):
        activity = InstallActivity(MainModel())
        qtbot.addWidget(activity)

    def test_no_install_prog(self, qtbot):
        setup_view: InstallActivity = InstallActivity(MainModel())
        qtbot.addWidget(setup_view)

        qtbot.mouseClick(setup_view.control_push_no_install, Qt.LeftButton)


class TestSubprojectsActivity:
    def test_is_renderable(self, qtbot):
        activity = SubprojectsActivity(MainModel())
        qtbot.addWidget(activity)

    def test_exit_subprojects(self, qtbot):
        setup_view: SubprojectsActivity = SubprojectsActivity(MainModel())
        qtbot.addWidget(setup_view)

        qtbot.mouseClick(setup_view.control_push_ok, Qt.LeftButton)
