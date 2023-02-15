from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon

from fileorganizer.python_extensions import make_resource_filepath


def make_icon_button(tooltip, icon, signal):
    button = QPushButton()
    button.setToolTip(tooltip)
    button.setIcon(QIcon(make_resource_filepath(icon)))
    button.clicked.connect(signal)
    return button
