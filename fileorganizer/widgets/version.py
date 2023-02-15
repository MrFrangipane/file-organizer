from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import QSize


class VersionWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.label = QLabel("VERSION")
        self.label2 = QLabel("number")

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.label)
        layout.addWidget(self.label2)

    def sizeHint(self):
        return QSize(80, 50)
