#!/usr/bin/env python3


#
# author : Michael Brockus.
# contact: <mailto:michaelbrockus@gmail.com>
# license: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0
#
# copyright 2020 The Meson-UI development team
#
class MesonUiNode:
    def __init__(self, data_ptr=None, next_ptr=None, prev_ptr=None):
        self.data = data_ptr
        self.next = next_ptr
        self.prev = prev_ptr


class MesonUiDLL:
    def __init__(self):
        self.head: MesonUiNode = None
        self.tail: MesonUiNode = None
        self.count: int = 0

    def is_empty(self):
        return self.head is None

    def append_item(self, data):
        new_item = MesonUiNode(data, None, None)
        if self.is_empty():
            self.head = new_item
            self.tail = self.head
        else:
            new_item.prev = self.tail
            self.tail.next = new_item
            self.tail = new_item
        self.count += 1

    def remove_item(self):
        if self.is_empty():
            return
        else:
            if self.head != self.tail:
                self.head = self.head.next
                self.head.previous = None
            else:
                self.head = self.tail = None
        self.count -= 1

    def iter(self):
        current = self.head
        while current:
            item_val = current.data
            current = current.next
            yield item_val

    def size(self):
        return self.count

    def search_for(self, key: str):
        if self.is_empty():
            return

        for node in self.iter():
            if key == node:
                return node
        return None
