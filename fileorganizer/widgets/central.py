from PySide6.QtWidgets import QWidget, QGridLayout

from fileorganizer.qt_extensions.widget_list import WidgetList

from fileorganizer.widgets.project import ProjectWidget
from fileorganizer.widgets.step import StepWidget
from fileorganizer.widgets.version import VersionWidget


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.projects = WidgetList("Project")
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

        self.projects.addWidget(ProjectWidget())
        self.projects.addWidget(ProjectWidget())
        self.projects.addWidget(ProjectWidget())
        self.projects.addWidget(ProjectWidget())
        self.projects.addWidget(ProjectWidget())
        self.projects.addWidget(ProjectWidget())
        self.projects.addWidget(ProjectWidget())

        self.steps.addWidget(StepWidget())
        self.steps.addWidget(StepWidget())
        self.steps.addWidget(StepWidget())
        self.steps.addWidget(StepWidget())
        self.steps.addWidget(StepWidget())
        self.steps.addWidget(StepWidget())

        self.versions.addWidget(VersionWidget())
        self.versions.addWidget(VersionWidget())
