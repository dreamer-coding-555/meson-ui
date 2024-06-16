#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from .buildoptions import IntroBuildOptionsTab
from .projectinfo import IntroProjectInfoTab
from .tests import IntroTestlogInfoTab


class IntrospectionDashboard:
    def __init__(self, context, meson_api):
        super().__init__()
        self._buildoptions: IntroBuildOptionsTab = IntroBuildOptionsTab(
            context=context, meson_api=meson_api
        )
        self._projectinfo: IntroProjectInfoTab = IntroProjectInfoTab(
            context=context, meson_api=meson_api
        )
        self._testloginfo: IntroTestlogInfoTab = IntroTestlogInfoTab(
            context=context, meson_api=meson_api
        )

    def update(self, meson_api: None):
        self._buildoptions.update_introspection(meson_api)
        self._projectinfo.update_introspection(meson_api)
        self._testloginfo.update_introspection(meson_api)
