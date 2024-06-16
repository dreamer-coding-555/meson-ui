#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#


class BackendImplementionApi:
    def __init__(self, meson_api):
        self.meson_api = meson_api

    @property
    def testinfo(self):
        return self.meson_api.get_object(group="tests", extract_method="loader")

    def generator(self):
        raise NotImplementedError('IDE Backend "generate" method not iemented!')

    def generate_project(self):
        raise NotImplementedError('IDE Backend "generate_project" method not iemented!')
