import os
import sys

from PySide6.QtWidgets import QApplication

from fileorganizer.python_extensions import make_resource_filepath
from fileorganizer.api.project import ProjectAPI
from fileorganizer.ui.main_window import MainWindow
from fileorganizer.ui.central import CentralWidget


_ROOT_FOLDER = sys.argv[1].replace("\\", os.sep).replace("/", os.sep)  # FIXME with argparse

#
# API
ProjectAPI.root_folder = _ROOT_FOLDER

#
# UI
with open(make_resource_filepath("stylesheet.qss"), "r") as stylesheet_file:
    stylesheet_content = stylesheet_file.read()

q_application = QApplication()
q_application.setStyleSheet(stylesheet_content)

main_window = MainWindow()
central_widget = CentralWidget()

main_window.setCentralWidget(central_widget)

#
# Run
if "--css" in sys.argv:
    from guibedos6.css.editor import CSSEditor
    css_editor = CSSEditor('Frangitron')

if "--maximized" in sys.argv:
    main_window.showMaximized()
else:
    main_window.show()

sys.exit(q_application.exec())
