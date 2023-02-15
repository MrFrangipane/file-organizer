from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import QSize


class StepWidget(QWidget):
    def __init__(self, name, parent=None):
        QWidget.__init__(self, parent)

        self.name = name
        self._label = QLabel(name)

        layout = QGridLayout(self)
        layout.addWidget(self._label)

    def sizeHint(self):
        return QSize(120, 60)
