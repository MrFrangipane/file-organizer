from PySide6.QtWidgets import QPushButton, QMessageBox
from PySide6.QtGui import QIcon

from fileorganizer.python_extensions import make_resource_filepath


def make_icon_button(tooltip, icon, signal, caption="", size=30) -> QPushButton:
    icon = QIcon(make_resource_filepath(icon))
    if caption:
        button = QPushButton(caption)
        button.setFixedHeight(size)
    else:
        button = QPushButton()
        button.setFixedSize(size, size)
    button.setToolTip(tooltip)
    button.setIcon(icon)
    button.clicked.connect(signal)
    return button


def make_warning_message_box(parent, message) -> QMessageBox:
    message_box = QMessageBox(parent)
    message_box.setIcon(QMessageBox.Icon.Warning)
    message_box.setWindowTitle("Warning")
    message_box.setText(message)
    message_box.setStandardButtons(QMessageBox.Ok)
    return message_box
