#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from pathlib import Path
from os.path import join
import pytest


from mesonui.mesonuilib.appconfig.core import MesonCoreConfig
from mesonui.mesonuilib.appconfig.base import MesonBaseConfig
from mesonui.mesonuilib.appconfig.test import MesonTestConfig
from mesonui.mesonuilib.appconfig.path import MesonPathConfig
from mesonui.mesonuilib.appconfig.dist import MesonDistConfig
from mesonui.mesonuilib.appconfig.init import MesonInitConfig
from mesonui.mesonuilib.appconfig.backend import MesonBackendConfig
from mesonui.mesonuilib.appconfig.install import MesonInstallConfig

from mesonui.mesonuilib.coredata import MesonUiCache
from mesonui.mesonuilib.coredata import MesonUiInitCache
from mesonui.mesonuilib.coredata import MesonUiDistCache
from mesonui.mesonuilib.coredata import MesonUiInstallCache
from mesonui.mesonuilib.mesonapi.buildoptions import MESON_OPTION_MACHINE
from mesonui.mesonuilib.mesonapi.buildoptions import MESON_OPTION_SECTION
from mesonui.mesonuilib.mesonapi.buildoptions import MESON_OPTION_TYPES
from mesonui.mesonuilib.mesonapi.buildoptions import BuildOption

from mesonui.repository.dataloader import MesonBuilddirLoader
from mesonui.repository.datareader import MesonBuilddirReader
from mesonui.repository.datascanner import MesonScriptReader
from mesonui.repository.mesonapi import MesonAPI
from mesonui.mesonuilib.buildsystem import Meson
from mesonui.containers.doublylist import MesonUiDLL
from mesonui.containers.queue import MesonUiQueue
from mesonui.containers.stack import MesonUiStack
from mesonui.mesonuilib.utilitylib import MesonUiException
from mesonui.mesonuilib.utilitylib import OSUtility


class TestBuildOptionWrapper:
    def test_integer(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)
        opt = option.integer("install_umask")

        assert opt.section in MESON_OPTION_SECTION
        assert opt.machine in MESON_OPTION_MACHINE
        assert opt.type in MESON_OPTION_TYPES

    def test_boolean(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)
        opt = option.boolean("strip")

        assert opt.section in MESON_OPTION_SECTION
        assert opt.machine in MESON_OPTION_MACHINE
        assert opt.type in MESON_OPTION_TYPES

    def test_string(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)
        opt = option.string("bindir")

        assert opt.section in MESON_OPTION_SECTION
        assert opt.machine in MESON_OPTION_MACHINE
        assert opt.type in MESON_OPTION_TYPES

    def test_combo(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)
        opt = option.combo("backend")

        assert opt.section in MESON_OPTION_SECTION
        assert opt.machine in MESON_OPTION_MACHINE
        assert opt.type in MESON_OPTION_TYPES

    def test_array(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)
        opt = option.array("cmake_prefix_path")

        assert opt.section in MESON_OPTION_SECTION
        assert opt.machine in MESON_OPTION_MACHINE
        assert opt.type in MESON_OPTION_TYPES

    def test_integer_wrong_type_name_pram(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)

        with pytest.raises(MesonUiException) as e:
            option.integer(None)
        assert "Option has wrong type <class 'NoneType'> should be string!" == str(
            e.value
        )

    def test_boolean_wrong_type_name_pram(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)

        with pytest.raises(MesonUiException) as e:
            option.boolean(None)
        assert "Option has wrong type <class 'NoneType'> should be string!" == str(
            e.value
        )

    def test_string_wrong_type_name_pram(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)

        with pytest.raises(MesonUiException) as e:
            option.string(None)
        assert "Option has wrong type <class 'NoneType'> should be string!" == str(
            e.value
        )

    def test_combo_wrong_type_name_pram(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)

        with pytest.raises(MesonUiException) as e:
            option.combo(None)
        assert "Option has wrong type <class 'NoneType'> should be string!" == str(
            e.value
        )

    def test_array_wrong_type_name_pram(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)

        with pytest.raises(MesonUiException) as e:
            option.array(None)
        assert "Option has wrong type <class 'NoneType'> should be string!" == str(
            e.value
        )

    def test_integer_option_not_found(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)

        with pytest.raises(MesonUiException) as e:
            option.integer("debug")
        assert "Option has wrong type!" == str(e.value)

    def test_boolean_option_not_found(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)

        with pytest.raises(MesonUiException) as e:
            option.integer("layout")
        assert "Option has wrong type!" == str(e.value)

    def test_string_option_not_found(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)

        with pytest.raises(MesonUiException) as e:
            option.integer("debug")
        assert "Option has wrong type!" == str(e.value)

    def test_combo_option_not_found(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)

        with pytest.raises(MesonUiException) as e:
            option.integer("debug")
        assert "Option has wrong type!" == str(e.value)

    def test_array_option_not_found(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)

        with pytest.raises(MesonUiException) as e:
            option.integer("debug")
        assert "Option has wrong type!" == str(e.value)

    def test_option_not_found(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        api: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        option: BuildOption = BuildOption(api)

        with pytest.raises(MesonUiException) as e:
            option.integer("smap-option")
        assert "Option smap-option not found!" == str(e.value)


class TestMesonUiQueue:
    def test_enqueue(self):
        queue: MesonUiQueue = MesonUiQueue()
        queue.enqueue("message log 1")

        assert len(queue.items) == 1

    def test_enqueue_copy(self):
        queue: MesonUiQueue = MesonUiQueue()
        queue.enqueue("message log 1")

        assert queue.enqueue("message log 1") is None
        assert len(queue.items) == 1

    def test_dequeue(self):
        queue: MesonUiQueue = MesonUiQueue()
        queue.enqueue("message log 1")
        queue.enqueue("message log 2")

        assert len(queue.items) == 2

        assert queue.dequeue() == "message log 1"
        assert len(queue.items) == 1

        assert queue.dequeue() == "message log 2"
        assert len(queue.items) == 0

    def test_dequeue_empty(self):
        queue: MesonUiQueue = MesonUiQueue()

        assert queue.dequeue() is None
        assert len(queue.items) == 0


class TestMesonUiStack:
    def test_push(self):
        stack: MesonUiStack = MesonUiStack()
        stack.push("--some-flag")

        assert stack.pop() == "--some-flag"

    def test_push_copy(self):
        stack: MesonUiStack = MesonUiStack()
        stack.push("--some-flag")

        assert stack.push("--some-flag") is False
        assert stack.pop() == "--some-flag"

    def test_pop_empty(self):
        stack: MesonUiStack = MesonUiStack()
        stack.push("--some-flag")

        assert stack.pop() == "--some-flag"
        assert stack.pop() is None


class TestMesonDll:
    def test_insert(self):
        dll: MesonUiDLL = MesonUiDLL()

        assert dll.is_empty() is True
        dll.append_item("ensert some data")

        assert dll.size() == 1
        assert dll.is_empty() is False

    def test_search(self):
        dll: MesonUiDLL = MesonUiDLL()

        assert dll.is_empty() is True
        dll.append_item("insert some data")

        assert dll.search_for("insert some data") == "insert some data"
        assert dll.search_for("spam data") is None
        assert dll.size() == 1
        assert dll.is_empty() is False

    def test_search_empty(self):
        dll: MesonUiDLL = MesonUiDLL()

        assert dll.is_empty() is True

        assert dll.search_for("not here") is None
        assert dll.size() == 0

    def test_remove(self):
        dll: MesonUiDLL = MesonUiDLL()

        assert dll.is_empty() is True
        dll.append_item("entry item 1")
        dll.append_item("entry item 2")
        dll.append_item("entry item 3")

        assert dll.size() == 3
        assert dll.is_empty() is False

        dll.remove_item()

        assert dll.size() == 2

    def test_remove_from_empty(self):
        dll: MesonUiDLL = MesonUiDLL()

        assert dll.is_empty() is True
        assert dll.size() == 0

        dll.remove_item()

        assert dll.size() == 0


class TestMesonAPI:
    def test_change_sourcedir(self):
        script: MesonAPI = MesonAPI("test/dir/one", "test/dir/one/builddir")

        assert script.sourcedir == "test/dir/one"
        assert script.builddir == "test/dir/one/builddir"

        script.sourcedir = "test/dir/two"
        script.builddir = "test/dir/two/builddir"

        assert script.sourcedir != "test/dir/one"
        assert script.builddir != "test/dir/one/builddir"
        assert script.sourcedir == "test/dir/two"
        assert script.builddir == "test/dir/two/builddir"

    def test_meson_api_scan_from_script(self):
        source = join("test-cases", "meson-api", "01-scan-script")
        build = join("test-cases", "meson-api", "01-scan-script", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        info = script.get_object(group="projectinfo", extract_method="script")

        assert info["descriptive_name"] == "simple-case"
        assert info["version"] == "0.1"
        assert info["subproject_dir"] == "subprojects"

    def test_meson_api_read_from_builddir(self):
        source = join("test-cases", "meson-api", "02-read-builddir")
        build = join("test-cases", "meson-api", "02-read-builddir", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        info = script.get_object(group="projectinfo", extract_method="reader")

        assert info["descriptive_name"] == "simple-case"
        assert info["version"] == "0.1"
        assert info["subproject_dir"] == "subprojects"

    def test_meson_api_load_from_builddir(self):
        source = join("test-cases", "meson-api", "03-load-builddir")
        build = join("test-cases", "meson-api", "03-load-builddir", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        info = script.get_object(group="projectinfo", extract_method="loader")

        assert info["descriptive_name"] == "simple-case"
        assert info["version"] == "0.1"
        assert info["subproject_dir"] == "subprojects"

    def test_meson_api_reader_use_fullback(self):
        source = join("test-cases", "meson-api", "04-read-fullback")
        build = join("test-cases", "meson-api", "04-read-fullback", "builddir")

        script: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        #
        # Should automatically use fullback if builddir not found
        info = script.get_object(group="projectinfo", extract_method="reader")

        assert info["descriptive_name"] == "simple-case"
        assert info["version"] == "0.1"
        assert info["subproject_dir"] == "subprojects"

    def test_meson_api_loader_use_fullback(self):
        source = join("test-cases", "meson-api", "05-load-fullback")
        build = join("test-cases", "meson-api", "05-load-fullback", "builddir")

        script: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        #
        # Should automatically use fullback if builddir not found
        info = script.get_object(group="projectinfo", extract_method="loader")

        assert info["descriptive_name"] == "simple-case"
        assert info["version"] == "0.1"
        assert info["subproject_dir"] == "subprojects"

    def test_meson_api_reader_fullback_get_none(self):
        source = join("test-cases", "meson-api", "06-read-null")
        build = join("test-cases", "meson-api", "06-read-null", "builddir")

        script: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        #
        # As a last posable value we will give None
        info = script.get_object(group="projectinfo", extract_method="reader")

        assert info is None

    def test_meson_api_loader_fullback_get_none(self):
        source = join("test-cases", "meson-api", "07-load-null")
        build = join("test-cases", "meson-api", "07-load-null", "builddir")

        script: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        #
        # As a last posable value we will give None
        info = script.get_object(group="projectinfo", extract_method="loader")

        assert info is None

    def test_meson_api_scanner_fullback_get_none(self):
        source = join("test-cases", "meson-api", "08-scan-null")
        build = join("test-cases", "meson-api", "08-scan-null", "builddir")

        script: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        #
        # As a last posable value we will give None
        info = script.get_object(group="projectinfo", extract_method="script")

        assert info is None

    def test_meson_api_reader_testlogs_get_none(self):
        source = join("test-cases", "meson-api", "09-read-testlog-null")
        build = join("test-cases", "meson-api", "09-read-testlog-null", "builddir")

        script: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        #
        # Posable value of passing testlog will be None
        info = script.get_object(group="testlog", extract_method="reader")

        assert info is None

    def test_meson_api_loader_testlogs_get_none(self):
        source = join("test-cases", "meson-api", "10-load-testlog-null")
        build = join("test-cases", "meson-api", "10-load-testlog-null", "builddir")

        script: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        #
        # Posable value of passing testlog will be None
        info = script.get_object(group="testlog", extract_method="loader")

        assert info is None

    def test_meson_api_scanner_testlogs_get_none(self):
        source = join("test-cases", "meson-api", "11-scan-testlog-null")
        build = join("test-cases", "meson-api", "11-scan-testlog-null", "builddir")

        script: MesonAPI = MesonAPI(sourcedir=source, builddir=build)
        #
        # Posable value of passing testlog will be None
        info = script.get_object(group="testlog", extract_method="script")

        assert info is None

    def test_meson_api_bad_extract_method(self):
        reader: MesonAPI = MesonAPI(None, None)
        with pytest.raises(Exception) as e:
            reader = reader.get_object(group="not-a-key", extract_method="not-a-method")
        assert 'Extract method not-a-method not found in Meson "JSON" API!' == str(
            e.value
        )

    def test_meson_api_bad_extract_method_type(self):
        reader: MesonAPI = MesonAPI(None, None)
        with pytest.raises(Exception) as e:
            reader = reader.get_object(group="not-a-key", extract_method=None)
        assert "API extract method <class 'NoneType'> is not valid type!" == str(
            e.value
        )

    def test_meson_api_bad_group_type(self):
        reader: MesonAPI = MesonAPI(None, None)
        with pytest.raises(Exception) as e:
            reader = reader.get_object(group=1234.09, extract_method="not-a-method")
        assert "API group key pair <class 'float'> is not valid type!" == str(e.value)


class TestApiBuilddirLoader:
    def test_loader_projectinfo(self):
        source = join("test-cases", "intro-loader", "01-projectinfo")
        build = join("test-cases", "intro-loader", "01-projectinfo", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirLoader = MesonBuilddirLoader(join(source, "builddir"))
        info = script.extract_from(group="projectinfo")

        assert info["descriptive_name"] == "simple-case"
        assert info["version"] == "0.1"
        assert info["subproject_dir"] == "subprojects"

    def test_loader_buildoptions(self):
        source = join("test-cases", "intro-loader", "04-buildoptions")
        build = join("test-cases", "intro-loader", "04-buildoptions", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirLoader = MesonBuilddirLoader(build)
        info = script.extract_from(group="buildoptions")

        assert info[0]["name"] == "auto_features"
        assert info[0]["value"] == "auto"

    def test_loader_meson_test(self):
        source = join("test-cases", "intro-loader", "02-unittests")
        build = join("test-cases", "intro-loader", "02-unittests", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirLoader = MesonBuilddirLoader(build)
        info = script.extract_from(group="tests")

        assert info[0]["name"] == "basic unit test"

    def test_loader_benchmarks(self):
        source = join("test-cases", "intro-loader", "03-benchmarks")
        build = join("test-cases", "intro-loader", "03-benchmarks", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirLoader = MesonBuilddirLoader(build)
        info = script.extract_from(group="benchmarks")

        assert info[0]["name"] == "basic benchmark"

    def test_loader_dependencies(self):
        source = join("test-cases", "intro-loader", "05-dependencies")
        build = join("test-cases", "intro-loader", "05-dependencies", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirLoader = MesonBuilddirLoader(build)
        info = script.extract_from(group="dependencies")

        assert info == []

    def test_loader_targets(self):
        source = join("test-cases", "intro-loader", "06-targets")
        build = join("test-cases", "intro-loader", "06-targets", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()
        meson.compile()
        meson.clean()

        script: MesonBuilddirLoader = MesonBuilddirLoader(build)
        info = script.extract_from(group="targets")

        assert info[0]["name"] == "prog"
        assert info[0]["type"] == "executable"
        assert info[0]["id"] == "prog@exe"

    def test_loader_install(self):
        source = join("test-cases", "intro-loader", "07-install")
        build = join("test-cases", "intro-loader", "07-install", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirLoader = MesonBuilddirLoader(build)
        info = script.extract_from(group="installed")

        assert info == {}

    def test_loader_mesoninfo(self):
        source = Path(join("test-cases", "intro-loader", "08-mesoninfo"))
        build = Path(join("test-cases", "intro-loader", "08-mesoninfo", "builddir"))
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirLoader = MesonBuilddirLoader(build)
        info = script.extract_from(group="meson-info")

        assert info["directories"]["source"] == str(source.resolve())
        assert info["directories"]["build"] == str(build.resolve())
        assert info["directories"]["info"] == str(join(build.resolve(), "meson-info"))

    def test_loader_no_testlogs(self):
        source = Path(join("test-cases", "intro-loader", "10-no-testlog"))
        build = Path(join("test-cases", "intro-loader", "10-no-testlog", "builddir"))
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirLoader = MesonBuilddirLoader(build)
        info = script.extract_from(group="testlog")

        assert info is None

    def test_loader_testlogs(self):
        source = Path(join("test-cases", "intro-loader", "09-testlog"))
        build = Path(join("test-cases", "intro-loader", "09-testlog", "builddir"))
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()
        meson.compile()
        meson.test()
        meson.clean()

        script: MesonBuilddirLoader = MesonBuilddirLoader(build)
        info = script.extract_from(group="testlog")

        assert info["name"] == "running test for testlog data"
        assert info["result"] == "OK"

    @pytest.mark.skipif(
        OSUtility.is_windows(), reason="Some issue with / char over \\ on Windows"
    )
    def test_loader_mesonbuild_files(self):
        source = Path(join("test-cases", "intro-loader", "11-buildsystem_files"))
        build = Path(
            join("test-cases", "intro-loader", "11-buildsystem_files", "builddir")
        )
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirLoader = MesonBuilddirLoader(build)
        info = script.extract_from(group="buildsystem-files")

        assert info[0] == join(source.resolve(), "meson.build")

    def test_loader_bad_extract_method(self):
        reader: MesonBuilddirLoader = MesonBuilddirLoader(None)
        with pytest.raises(Exception) as e:
            reader = reader.extract_from(group="not-a-key")
        assert "Group tag not-a-key not found in extract via data options!" == str(
            e.value
        )


class TestApiBuilddirReader:

    def test_reader_projectinfo(self):
        source = join("test-cases", "intro-reader", "01-projectinfo")
        build = join("test-cases", "intro-reader", "01-projectinfo", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirReader = MesonBuilddirReader(join(source, "builddir"))
        info = script.extract_from(group="projectinfo")

        assert info["descriptive_name"] == "simple-case"
        assert info["version"] == "0.1"
        assert info["subproject_dir"] == "subprojects"

    def test_reader_buildoptions(self):
        source = join("test-cases", "intro-reader", "04-buildoptions")
        build = join("test-cases", "intro-reader", "04-buildoptions", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirReader = MesonBuilddirReader(build)
        info = script.extract_from(group="buildoptions")

        assert info[0]["name"] == "auto_features"
        assert info[0]["value"] == "auto"

    def test_reader_meson_test(self):
        source = join("test-cases", "intro-reader", "02-unittests")
        build = join("test-cases", "intro-reader", "02-unittests", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirReader = MesonBuilddirReader(build)
        info = script.extract_from(group="tests")

        assert info[0]["name"] == "basic unit test"

    def test_reader_benchmarks(self):
        source = join("test-cases", "intro-reader", "03-benchmarks")
        build = join("test-cases", "intro-reader", "03-benchmarks", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirReader = MesonBuilddirReader(build)
        info = script.extract_from(group="benchmarks")

        assert info[0]["name"] == "basic benchmark"

    def test_reader_dependencies(self):
        source = join("test-cases", "intro-reader", "05-dependencies")
        build = join("test-cases", "intro-reader", "05-dependencies", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirReader = MesonBuilddirReader(build)
        info = script.extract_from(group="dependencies")

        assert info == []

    def test_reader_scan_dependencies(self):
        source = join("test-cases", "intro-reader", "06-scan-dependencies")
        build = join("test-cases", "intro-reader", "06-scan-dependencies", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirReader = MesonBuilddirReader(build)
        info = script.extract_from(group="scan-dependencies")

        assert info == {}

    def test_reader_targets(self):
        source = join("test-cases", "intro-reader", "07-targets")
        build = join("test-cases", "intro-reader", "07-targets", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirReader = MesonBuilddirReader(build)
        info = script.extract_from(group="targets")

        assert info[0]["name"] == "prog"
        assert info[0]["type"] == "executable"
        assert info[0]["id"] == "prog@exe"

    def test_reader_install(self):
        source = join("test-cases", "intro-reader", "08-install")
        build = join("test-cases", "intro-reader", "08-install", "builddir")
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirReader = MesonBuilddirReader(build)
        info = script.extract_from(group="installed")

        assert info == {}

    @pytest.mark.skipif(
        OSUtility.is_windows(), reason="Some issue with / char over \\ on Windows"
    )
    def test_reader_mesonbuild_files(self):
        source = Path(join("test-cases", "intro-reader", "09-buildsystem_files"))
        build = Path(
            join("test-cases", "intro-reader", "09-buildsystem_files", "builddir")
        )
        meson: Meson = Meson(sourcedir=source, builddir=build)

        meson.setup()

        script: MesonBuilddirReader = MesonBuilddirReader(build)
        info = script.extract_from(group="buildsystem-files")
        print(info)
        assert info[0] == join(source.resolve(), "meson.build")

    def test_reader_bad_extract_method(self):
        reader: MesonBuilddirReader = MesonBuilddirReader(None)
        with pytest.raises(Exception) as e:
            reader = reader.extract_from(group="not-a-key")
        assert "Group tag not-a-key not found in extract via data options!" == str(
            e.value
        )


class TestApiScriptScanner:

    def test_script_projectinfo(self):
        script: MesonScriptReader = MesonScriptReader(
            join("test-cases", "intro-scanner", "01-projectinfo")
        )
        info = script.extract_from(group="projectinfo")

        assert info["descriptive_name"] == "simple-case"
        assert info["version"] == "0.1"
        assert info["subproject_dir"] == "subprojects"

    def test_script_buildoptions(self):
        script: MesonScriptReader = MesonScriptReader(
            join("test-cases", "intro-scanner", "04-buildoptions")
        )
        info = script.extract_from(group="buildoptions")

        assert info[0]["name"] == "auto_features"
        assert info[0]["value"] == "auto"

    def test_meson_test(self):
        script: MesonScriptReader = MesonScriptReader(
            join("test-cases", "intro-scanner", "02-unittests")
        )
        info = script.extract_from(group="tests")

        assert info == {}

    def test_script_benchmarks(self):
        script: MesonScriptReader = MesonScriptReader(
            join("test-cases", "intro-scanner", "03-benchmarks")
        )
        info = script.extract_from(group="benchmarks")

        assert info == {}

    def test_script_dependencies(self):
        script: MesonScriptReader = MesonScriptReader(
            join("test-cases", "intro-scanner", "05-dependencies")
        )
        info = script.extract_from(group="dependencies")

        assert info == []

    def test_script_scan_dependencies(self):
        script: MesonScriptReader = MesonScriptReader(
            join("test-cases", "intro-scanner", "06-scan-dependencies")
        )
        info = script.extract_from(group="scan-dependencies")

        assert info == []

    def test_script_targets(self):
        script: MesonScriptReader = MesonScriptReader(
            join("test-cases", "intro-scanner", "07-targets")
        )
        info = script.extract_from(group="targets")

        assert info[0]["name"] == "prog"
        assert info[0]["type"] == "executable"
        assert info[0]["id"] == "prog@exe"

    def test_script_bad_extract_method(self):
        reader: MesonScriptReader = MesonScriptReader(None)
        with pytest.raises(Exception) as e:
            reader = reader.extract_from(group="not-a-key")
        assert "Group tag not-a-key not found in extract via data options!" == str(
            e.value
        )


class TestMesonCacheConfig:
    def test_core_configure(self):
        conf = MesonCoreConfig()

        for i in conf.meson_configure:
            assert conf.meson_configure[i] is None

        with pytest.raises(MesonUiException) as e:
            conf.extract()
        assert 'Meson cache failed do to "None" value found while loading value' == str(
            e.value
        )

    def test_base_configure(self):
        conf = MesonBaseConfig()

        for i in conf.meson_configure:
            assert conf.meson_configure[i] is None

        with pytest.raises(MesonUiException) as e:
            conf.extract()
        assert 'Meson cache failed do to "None" value found while loading value' == str(
            e.value
        )

    def test_path_configure(self):
        conf = MesonPathConfig()

        for i in conf.meson_configure:
            assert conf.meson_configure[i] is None

        with pytest.raises(MesonUiException) as e:
            conf.extract()
        assert 'Meson cache failed do to "None" value found while loading value' == str(
            e.value
        )

    def test_test_configure(self):
        conf = MesonTestConfig()

        for i in conf.meson_configure:
            assert conf.meson_configure[i] is None

        with pytest.raises(MesonUiException) as e:
            conf.extract()
        assert 'Meson cache failed do to "None" value found while loading value' == str(
            e.value
        )

    def test_init_configure(self):
        conf = MesonInitConfig()

        for i in conf.meson_configure:
            assert conf.meson_configure[i] is None

        with pytest.raises(MesonUiException) as e:
            conf.extract()
        assert 'Meson cache failed do to "None" value found while loading value' == str(
            e.value
        )

    def test_dist_configure(self):
        conf = MesonDistConfig()

        for i in conf.meson_configure:
            assert conf.meson_configure[i] is None

        with pytest.raises(MesonUiException) as e:
            conf.extract()
        assert 'Meson cache failed do to "None" value found while loading value' == str(
            e.value
        )

    def test_install_configure(self):
        conf = MesonInstallConfig()

        for i in conf.meson_configure:
            assert conf.meson_configure[i] is None

        with pytest.raises(MesonUiException) as e:
            conf.extract()
        assert 'Meson cache failed do to "None" value found while loading value' == str(
            e.value
        )

    def test_backend_configure(self):
        conf = MesonBackendConfig()

        for i in conf.meson_configure:
            assert conf.meson_configure[i] is None

        with pytest.raises(MesonUiException) as e:
            conf.extract()
        assert 'Meson cache failed do to "None" value found while loading value' == str(
            e.value
        )

    def test_core_configure_if_empty_option(self):
        conf = MesonCoreConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("", "some-value")
        assert "Option key passed as empty string object" == str(e.value)

    def test_base_configure_if_empty_option(self):
        conf = MesonBaseConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("", "some-value")
        assert "Option key passed as empty string object" == str(e.value)

    def test_path_configure_if_empty_option(self):
        conf = MesonPathConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("", "some-value")
        assert "Option key passed as empty string object" == str(e.value)

    def test_test_configure_if_empty_option(self):
        conf = MesonTestConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("", "some-value")
        assert "Option key passed as empty string object" == str(e.value)

    def test_init_configure_if_empty_option(self):
        conf = MesonInitConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("", "some-value")
        assert "Option key passed as empty string object" == str(e.value)

    def test_dist_configure_if_empty_option(self):
        conf = MesonDistConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("", "some-value")
        assert "Option key passed as empty string object" == str(e.value)

    def test_install_configure_if_empty_option(self):
        conf = MesonInstallConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("", "some-value")
        assert "Option key passed as empty string object" == str(e.value)

    def test_backend_configure_if_empty_option(self):
        conf = MesonBackendConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("", "some-value")
        assert "Option key passed as empty string object" == str(e.value)

    def test_core_configure_if_empty_value(self):
        conf = MesonCoreConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("some-option", "")
        assert "Value passed in as empty string object" == str(e.value)

    def test_base_configure_if_empty_value(self):
        conf = MesonBaseConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("some-option", "")
        assert "Value passed in as empty string object" == str(e.value)

    def test_path_configure_if_empty_value(self):
        conf = MesonPathConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("some-option", "")
        assert "Value passed in as empty string object" == str(e.value)

    def test_test_configure_if_empty_value(self):
        conf = MesonTestConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("some-option", "")
        assert "Value passed in as empty string object" == str(e.value)

    def test_init_configure_if_empty_value(self):
        conf = MesonInitConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("some-option", "")
        assert "Value passed in as empty string object" == str(e.value)

    def test_dist_configure_if_empty_value(self):
        conf = MesonDistConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("some-option", "")
        assert "Value passed in as empty string object" == str(e.value)

    def test_install_configure_if_empty_value(self):
        conf = MesonInstallConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("some-option", "")
        assert "Value passed in as empty string object" == str(e.value)

    def test_backend_configure_if_empty_value(self):
        conf = MesonBackendConfig()

        with pytest.raises(MesonUiException) as e:
            conf.config("some-option", "")
        assert "Value passed in as empty string object" == str(e.value)


class TestMesonUiCacheSystem:
    def test_mesonui_main_cache(self):
        cache = MesonUiCache()
        cache.init_cache()

        assert cache.get_core() is not None
        assert cache.get_base() is not None
        assert cache.get_path() is not None
        assert cache.get_test() is not None
        assert cache.get_backend() is not None

    def test_init_cache(self):
        cache = MesonUiInitCache()
        cache.init_cache()
        values = cache.get_cache()

        for i in values:
            assert values[i] is not None

    def test_dist_cache(self):
        cache = MesonUiDistCache()
        cache.init_cache()
        values = cache.get_cache()

        for i in values:
            assert values[i] is not None

    def test_install_cache(self):
        cache = MesonUiInstallCache()
        cache.init_cache()
        values = cache.get_cache()

        for i in values:
            assert values[i] is not None

    def test_init_cache_give_exception(self):
        cache = MesonUiInitCache()

        with pytest.raises(MesonUiException) as e:
            cache.get_cache()
        assert 'Meson cache failed do to "None" value found while loading value' == str(
            e.value
        )

    def test_dist_cache_give_exception(self):
        cache = MesonUiDistCache()

        with pytest.raises(MesonUiException) as e:
            cache.get_cache()
        assert 'Meson cache failed do to "None" value found while loading value' == str(
            e.value
        )

    def test_install_cache_give_exception(self):
        cache = MesonUiInstallCache()

        with pytest.raises(MesonUiException) as e:
            cache.get_cache()
        assert 'Meson cache failed do to "None" value found while loading value' == str(
            e.value
        )
