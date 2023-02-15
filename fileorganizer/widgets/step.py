from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import QSize


class StepWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.label = QLabel("STEP")
        self.label2 = QLabel("Name")

        layout = QGridLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.label2)

    def sizeHint(self):
        return QSize(80, 80)
