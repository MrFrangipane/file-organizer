from PySide6.QtWidgets import QInputDialog
from PySide6.QtCore import QObject, Signal

from fileorganizer.qt_extensions import make_warning_message_box
from fileorganizer.api.project import ProjectAPI


class Application(QObject):
    """
    Coordinates API and UI
    """

    projectCreated = Signal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        self.main_window = None
        self.root_folder = None

    def project_new(self):
        project_name, ok = QInputDialog().getText(self.main_window, "New Project", "Name:")
        if not ok or not project_name:
            return

        if ProjectAPI.exists(project_name):
            make_warning_message_box(self.main_window, f"The project {project_name} already exists").exec()
            return

        if ProjectAPI.new(project_name):
            self.projectCreated.emit()
        else:
            make_warning_message_box(self.main_window, f"Error during project creation").exec()
