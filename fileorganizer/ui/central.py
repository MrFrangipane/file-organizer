from PySide6.QtWidgets import QWidget, QGridLayout, QInputDialog

from fileorganizer.qt_extensions import make_warning_message_box
from fileorganizer.qt_extensions.widget_list import WidgetList
from fileorganizer.qt_extensions.hourglass import Hourglass

from fileorganizer.ui.project import ProjectWidget
from fileorganizer.ui.step import StepWidget
from fileorganizer.ui.version import VersionWidget

from fileorganizer.api.project import ProjectAPI
from fileorganizer.api.step import StepAPI
from fileorganizer.api.version import VersionAPI


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.projects = WidgetList("Project")
        self.projects.newClicked.connect(self.project_new)
        self.projects.currentChanged.connect(self.steps_refresh)
        self.projects.refreshClicked.connect(self.projects_refresh)
        self.projects.documentationClicked.connect(self.project_documentation)

        self.steps = WidgetList("Step", horizontal=True)
        self.steps.newClicked.connect(self.step_new)
        self.steps.currentChanged.connect(self.versions_refresh)
        self.steps.refreshClicked.connect(self.steps_refresh)
        self.steps.documentationClicked.connect(self.step_documentation)

        self.versions = WidgetList("Version")
        self.versions.newClicked.connect(self.version_new)
        self.versions.refreshClicked.connect(self.versions_refresh)
        self.versions.documentationClicked.connect(self.version_documentation)

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

    def project_new(self):
        project_name, ok = QInputDialog().getText(self.parent(), "New Project", "Name:")
        if not ok or not project_name:
            return

        if ProjectAPI.exists(project_name):
            make_warning_message_box(self.parent(), f"The project {project_name} already exists").exec()
            return

        if ProjectAPI.new(project_name):
            self.projects_refresh()
        else:
            make_warning_message_box(self.parent(), f"Error during project creation").exec()

    def projects_refresh(self):
        with Hourglass():
            self.versions.clear()
            self.steps.clear()
            self.projects.clear()
            for project_name in ProjectAPI.all_names():
                self.projects.addWidget(ProjectWidget(project_name))

    def project_documentation(self):
        project_name = self.projects.selected()
        if project_name:
            ProjectAPI.open_documentation(project_name)

    def step_new(self):
        project_name = self.projects.selected()
        if project_name is None:
            return

        step_name, ok = QInputDialog().getText(self.parent(), "New Step", "Name:")
        if not ok or not step_name:
            return

        if StepAPI.exists(project_name, step_name):
            make_warning_message_box(
                self.parent(),
                f"The step {step_name} already exists for project {project_name}"
            ).exec()
            return

        if StepAPI.new(project_name, step_name):
            self.steps_refresh()
        else:
            make_warning_message_box(self.parent(), f"Error during step creation").exec()

    def steps_refresh(self):
        with Hourglass():
            project_name = self.projects.selected()
            if project_name is None:
                return

            self.versions.clear()
            self.steps.clear()

            for step_name in StepAPI.all_names(project_name):
                self.steps.addWidget(StepWidget(step_name))

    def step_documentation(self):
        project_name = self.projects.selected()
        step_name = self.steps.selected()
        if project_name and step_name:
            StepAPI.open_documentation(project_name, step_name)

    def version_new(self):
        project_name = self.projects.selected()
        step_name = self.steps.selected()
        if project_name is None or step_name is None:
            return

        version_name, ok = QInputDialog().getText(self.parent(), "New Version", "Name:")
        if not ok or not version_name:
            return

        if VersionAPI.exists(project_name, step_name, version_name):
            make_warning_message_box(
                self.parent(),
                f"The version {version_name} already exists for step {project_name}/{step_name}"
            ).exec()
            return

        if VersionAPI.new(project_name, step_name, version_name):
            self.versions_refresh()
        else:
            make_warning_message_box(self.parent(), f"Error during version creation").exec()

    def versions_refresh(self):
        with Hourglass():
            project_name = self.projects.selected()
            step_name = self.steps.selected()
            if project_name is None or step_name is None:
                return

            self.versions.clear()
            for version_name in VersionAPI.all_names(project_name, step_name):
                self.versions.addWidget(VersionWidget(version_name))

    def version_documentation(self):
        project_name = self.projects.selected()
        step_name = self.steps.selected()
        version_name = self.versions.selected()
        if project_name and step_name and version_name:
            VersionAPI.open_documentation(project_name, step_name, version_name)
