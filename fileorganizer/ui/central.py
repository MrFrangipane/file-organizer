from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QInputDialog

from fileorganizer.qt_extensions import make_warning_message_box
from fileorganizer.qt_extensions.list import List
from fileorganizer.qt_extensions.hourglass import Hourglass

from fileorganizer.qt_extensions.list_item import ListItem
from fileorganizer.qt_extensions.notes_editor import NotesEditor
from fileorganizer.ui.version_details import VersionDetails

from fileorganizer.api.project import ProjectAPI
from fileorganizer.api.step import StepAPI
from fileorganizer.api.version import VersionAPI
from fileorganizer.api.contextual_action import ContextualActionAPI


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.projects = List("Project")
        self.projects.newClicked.connect(self.project_new)
        self.projects.refreshClicked.connect(self.projects_refresh)
        self.projects.currentChanged.connect(self.projects_current_changed)

        self.project_notes = NotesEditor("Notes")

        self.steps = List("Step")
        self.steps.newClicked.connect(self.step_new)
        self.steps.refreshClicked.connect(self.steps_refresh)
        self.steps.currentChanged.connect(self.steps_current_changed)

        self.step_notes = NotesEditor("Notes")

        self.versions = List("Version")
        self.versions.newClicked.connect(self.version_new)
        self.versions.refreshClicked.connect(self.versions_refresh)
        self.versions.currentChanged.connect(self.version_current_changed)

        self.version_notes = NotesEditor("Notes")

        self.version_details = VersionDetails()
        self.version_details.setMinimumSize(400, 400)
        self.version_details.copyFilepathClicked.connect(self.version_detail_copy_filepath)

        layout = QGridLayout(self)

        layout.addWidget(self.projects, 0, 0)
        layout.addWidget(self.steps, 1, 0)
        layout.addWidget(self.versions, 2, 0)

        layout.addWidget(self.project_notes, 0, 1)
        layout.addWidget(self.step_notes, 1, 1)
        layout.addWidget(self.version_notes, 2, 1)

        layout.addWidget(self.version_details, 0, 2, 3, 1)

        layout.setColumnStretch(2, 100)

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

    def projects_current_changed(self):
        project_name = self.projects.selected()
        self.project_notes.set_entity(project_name=project_name)
        self.steps_refresh()

    def projects_refresh(self):
        with Hourglass():
            self.version_details.clear()
            self.versions.clear()
            self.steps.clear()
            self.projects.clear()
            self.project_notes.clear()
            for project_name in ProjectAPI.all_names():
                item = ListItem(project_name)
                item.openFolderClicked.connect(self.project_open_folder)
                item.pathToClipboardClicked.connect(self.project_path_to_clipboard)
                self.projects.addItem(item)

    def project_open_folder(self):
        project_name = self.sender().name
        if project_name:
            ProjectAPI.open_folder(project_name)

    def project_path_to_clipboard(self):
        project_name = self.sender().name
        if project_name is None:
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(ProjectAPI.make_foldername(project_name))

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

    def steps_current_changed(self):
        project_name = self.projects.selected()
        step_name = self.steps.selected()
        self.step_notes.set_entity(project_name=project_name, step_name=step_name)
        self.versions_refresh()

    def steps_refresh(self):
        with Hourglass():
            self.version_details.clear()
            self.versions.clear()
            self.steps.clear()

            project_name = self.projects.selected()
            if project_name is None:
                return

            for step_name in StepAPI.all_names(project_name):
                item = ListItem(step_name)
                item.openFolderClicked.connect(self.step_open_folder)
                item.pathToClipboardClicked.connect(self.step_path_to_clipboard)
                self.steps.addItem(item)

    def step_open_folder(self):
        project_name = self.projects.selected()
        step_name = self.sender().name
        if project_name and step_name:
            StepAPI.open_folder(project_name, step_name)

    def step_path_to_clipboard(self):
        project_name = self.projects.selected()
        step_name = self.sender().name
        if step_name is None or project_name is None:
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(StepAPI.make_foldername(project_name, step_name))

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
            self.versions.clear()

            project_name = self.projects.selected()
            step_name = self.steps.selected()
            if project_name is None or step_name is None:
                return

            for version_name in VersionAPI.all_names(project_name, step_name):
                item = ListItem(version_name)
                item.openFolderClicked.connect(self.version_open_folder)
                item.pathToClipboardClicked.connect(self.version_path_to_clipboard)
                self.versions.addItem(item)

    def version_current_changed(self):
        self.version_details.clear()
        project_name = self.projects.selected()
        step_name = self.steps.selected()
        version_name = self.versions.selected()
        if not version_name:
            return

        self.version_notes.set_entity(project_name, step_name, version_name)

        self.version_details.set_filepath(VersionAPI.make_filepath(project_name, step_name, version_name))
        for action_widget in ContextualActionAPI.get_all_widgets(project_name, step_name, version_name):
            self.version_details.add_contextual_action_widget(action_widget)

    def version_open_folder(self):
        project_name = self.projects.selected()
        step_name = self.steps.selected()
        version_name = self.sender().name
        if project_name and step_name and version_name:
            VersionAPI.open_folder(project_name, step_name, version_name)

    def version_path_to_clipboard(self):
        project_name = self.projects.selected()
        step_name = self.steps.selected()
        version_name = self.sender().name
        if step_name is None or project_name is None or version_name is None:
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(VersionAPI.make_foldername(project_name, step_name, version_name))

    def version_detail_copy_filepath(self):
        filepath = self.version_details.filepath()
        if not filepath:
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(filepath)

    def version_notes_changed(self):
        project_name = self.projects.selected()
        step_name = self.steps.selected()
        version_name = self.versions.selected()
        if step_name is None or project_name is None or version_name is None:
            return
