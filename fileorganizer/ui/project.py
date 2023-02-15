from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import QSize


class ProjectWidget(QWidget):
    def __init__(self, project_name, parent=None):
        QWidget.__init__(self, parent)

        self.name = project_name
        self._label = QLabel(project_name)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._label)

    def sizeHint(self):
        return QSize(150, 40)
