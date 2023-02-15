from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon

from fileorganizer.python_extensions import make_resource_filepath


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle("File Organizer")
        self.setWindowIcon(QIcon(make_resource_filepath("stack.png")))
