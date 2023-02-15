from PySide6.QtWidgets import QApplication

from fileorganizer.widgets.main_window import MainWindow
from fileorganizer.widgets.central import CentralWidget
from fileorganizer.python_extensions import make_resource_filepath


with open(make_resource_filepath("stylesheet.qss"), "r") as stylesheet_file:
    stylesheet_content = stylesheet_file.read()

app = QApplication()

main_window = MainWindow()
main_window.setCentralWidget(CentralWidget())
main_window.setStyleSheet(stylesheet_content)
main_window.show()

app.exec()
