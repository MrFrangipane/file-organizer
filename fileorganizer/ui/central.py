from PySide6.QtWidgets import QWidget, QGridLayout

from fileorganizer.qt_extensions.widget_list import WidgetList
from fileorganizer.qt_extensions.hourglass import Hourglass

from fileorganizer.ui.project import ProjectWidget
from fileorganizer.ui.step import StepWidget
from fileorganizer.ui.version import VersionWidget

from fileorganizer.api.project import ProjectAPI


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.projects = WidgetList("Project")
        self.projects.refreshClicked.connect(self.projects_refresh)
        self.projects.documentationClicked.connect(self.project_documentation)

        self.steps = WidgetList("Step", horizontal=True)

        self.versions = WidgetList("Version")

        self.empty_version = QWidget()
        self.empty_version.setMinimumSize(400, 400)

        layout = QGridLayout(self)
        layout.addWidget(self.projects, 0, 0, 2, 1)
        layout.addWidget(self.steps, 0, 1, 1, 2)
        layout.addWidget(self.versions, 1, 2, 1, 1)
        layout.addWidget(self.empty_version, 1, 1)
        layout.setRowStretch(1, 100)
        layout.setColumnStretch(1, 100)

        self.projects_refresh()

    def projects_refresh(self):
        with Hourglass():
            self.projects.clear()
            for project_name in ProjectAPI.all_names():
                self.projects.addWidget(ProjectWidget(project_name))

    def project_documentation(self):
        selected_project_name = self.projects.selected()
        if selected_project_name:
            ProjectAPI.open_documentation(selected_project_name)
