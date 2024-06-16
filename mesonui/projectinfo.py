#!/usr/bin/env python3

#
# author : Michael Brockus.  
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#


info = '''\
Meson-UI is an open source build GUI meant to be both extremely fast,
and, even more importantly, as user friendly as possible.

The main design point of Meson-UI is to provide a standalone portable
build GUI and allow the user to access all or most of Meson build
systems features.
'''

class ProjectInfo:
    def get_description(self) -> str:
        return info

    def get_version(self) -> str:
        return '0.20.2'

    def get_license(self) -> str:
        return 'Apache-2.0'

    def get_project_name(self) -> str:
        return 'meson-ui'

    def get_packages(self) -> list:
        return ['mesonui',
                'mesonui.containers',
                'mesonui.dashboard',
                'mesonui.mesonuilib',
                'mesonui.repository',
                'mesonui.models',
                'mesonui.view',
                'mesonui.ui',
                'mesonui.mesonuilib.appconfig',
                'mesonui.mesonuilib.backends',
                'mesonui.mesonuilib.ninjabuild',
                'mesonui.mesonuilib.mesonbuild',
                'mesonui.mesonuilib.mesonapi']
