from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import QSize, Signal

from fileorganizer.qt_extensions import make_icon_button


class ListItem(QWidget):

    openFolderClicked = Signal()
    pathToClipboardClicked = Signal()

    def __init__(self, name, parent=None):
        QWidget.__init__(self, parent)

        self.name = name
        self._label = QLabel(name)
        self._label.setStyleSheet("color: rgb(230, 230, 230); padding:0")  # FIXME use a QSS property

        self._button_open_folder = make_icon_button(
            "Open folder in file explorer", 'folder.png',
            self.openFolderClicked,
            size=22  # FIXME constant ?
        )
        self._button_open_folder.setProperty("transparent", True)
        self._button_path_to_clipboard = make_icon_button(
            "Copy path to clipboard", 'clipboard-folder.png',
            self.pathToClipboardClicked,
            size=22
        )
        self._button_path_to_clipboard.setProperty("transparent", True)

        layout = QGridLayout(self)
        layout.addWidget(self._label)
        layout.addWidget(self._button_open_folder, 0, 1)
        layout.addWidget(self._button_path_to_clipboard, 0, 2)
        layout.setColumnStretch(0, 100)

    def sizeHint(self):
        return QSize(200, 40)
