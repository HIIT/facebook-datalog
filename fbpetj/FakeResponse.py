import sys

class FakeResponse:
    def __init__(self):
        if sys.version_info >= (3,0):
            self._content = bytes("{}","ascii")
            self._empty = bytes("","ascii") # return this if someone accidentally calls read() twice
        else:
            self._content = "{}"
            self._empty = ""
        self._isRead = False
    def read(self):
        if self._isRead:
            return self._empty
        else:
            self._isRead = True
            return self._content #no need to deep copy, since usage is intended to be like urllib's responses' read()
