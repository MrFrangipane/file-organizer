from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QGroupBox, QGridLayout, QLabel

from fileorganizer.qt_extensions import make_icon_button


class VersionDetails(QGroupBox):  # FIXME find a better name

    copyFilepathClicked = Signal()

    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)

        self.setTitle("Version details")

        self.label_filepath = QLabel()

        self.button_copy_filepath = make_icon_button(
            "Copy filepath to clipboard",
            "clipboard.png",
            self.copyFilepathClicked
        )

        layout = QGridLayout(self)
        layout.addWidget(self.label_filepath, 0, 0)
        layout.addWidget(self.button_copy_filepath, 0, 1)
        layout.addWidget(QWidget(), 1, 0, 1, 2)
        layout.setColumnStretch(0, 100)
        layout.setRowStretch(1, 100)

    def clear(self):
        self.label_filepath.clear()

    def set_filepath(self, filepath):
        self.label_filepath.setText(filepath)
        self.label_filepath.setToolTip(filepath)

    def filepath(self):
        return self.label_filepath.text()
