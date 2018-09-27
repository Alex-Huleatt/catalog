from collections import defaultdict

class Bitset:
    def __init__(self, chunk_size = 2**10, intbits = 32):
        self.chunks = defaultdict(lambda:[0]*chunk_size)
        self.chunk_size = chunk_size
        self.intbits = intbits

    def set_index(self, k, b):
        chunk = k // self.chunk_size
        r = k % self.chunk_size
        int_index = r // self.intbits
        bit_index = r % self.intbits
        if b:
            self.chunks[chunk][int_index] |= (1 << (self.intbits - bit_index))
        else:
            self.chunks[chunk][int_index] &= ~(1 << (self.intbits - bit_index))

    def add(self, k):
        self.set_index(k, 1)

    def remove(self, k):
        self.set_index(k, 0)

    def contains(self, k):
        chunk = k // self.chunk_size
        r = k % self.chunk_size
        int_index = r // self.intbits
        bit_index = r % self.intbits
        return bool(self.chunks[chunk][int_index] & (1 << (self.intbits - bit_index)))

    def __iter__(self):
        for k in self.chunks:
            for i in xrange(self.chunk_size):
                v = self.chunks[k][i]
                if v:
                    for j in range(self.intbits):
                        if v & (1 << (self.intbits - j)):
                            yield (k * self.chunk_size) + (i * self.intbits) + j

    def __or__(self, notself):
        b = Bitset()
        for c in self:
            b.add(c)
        for c in notself:
            b.add(c)

    def __and__(self, notself):
        b = Bitset()
        for c in self:
            if c in notself:
                b.add(c)

class TagManager:
    def __init__(self):
        self.tags = defaultdict(Bitset)

    def addK(self, k, tagset):
        for t in tagset:
            self.tags[t].add(k)

    def filter(self, tagset, starting=None):
        matching = starting
        for t in tagset:
            if matching:
                matching = matching & self.tags[t]
            else:
                matching = self.tags[t]
        return matching

import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QGridLayout(self)

    def setCell(self, path, y, x):
        label = QLabel(self)
        pixmap = QPixmap(path).scaled(64, 64, Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        self.layout.addWidget(label, y, x)

app = QApplication(sys.argv)
window = Window()
window.setGeometry(500, 300, 300, 300)
window.setCell('1.png', 2,3)
window.setCell('2.png', 3,3)
window.show()
sys.exit(app.exec_())
