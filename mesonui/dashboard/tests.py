#!/usr/bin/env python3

#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
from PyQt5.QtWidgets import QListWidgetItem


class IntroTestlogInfoTab:
    def __init__(self, context, meson_api):
        super().__init__()
        self._context = context
        self.setup_introspection()

    def setup_introspection(self):
        head_ref = self._context._model.model_testlogsinfo().get_list().head
        while head_ref is not None:
            new_item = QListWidgetItem(head_ref.data)
            self._context.testsinfo_list.addItem(new_item)
            head_ref = head_ref.next

    def update_introspection(self, meson_api):
        if self._context.testsinfo_list.count() != 0:
            self._context.testsinfo_list.clear()
        self._context._model.model_testlogsinfo().set_list(meson_api)

        head_ref = self._context._model.model_testlogsinfo().get_list().head
        if head_ref is None:
            new_item = QListWidgetItem("No Testlogs data.")
            self._context.testsinfo_list.addItem(new_item)
            return

        while head_ref is not None:
            new_item = QListWidgetItem(head_ref.data)
            self._context.testsinfo_list.addItem(new_item)
            head_ref = head_ref.next
