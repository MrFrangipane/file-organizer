from PySide6.QtWidgets import QGroupBox, QGridLayout, QPlainTextEdit

from fileorganizer.api.project import ProjectAPI
from fileorganizer.api.step import StepAPI
from fileorganizer.api.version import VersionAPI


class NotesEditor(QGroupBox):

    def __init__(self, title, parent=None):
        QGroupBox.__init__(self, parent)

        self.setTitle(title)

        self._notes = QPlainTextEdit()
        self._notes.textChanged.connect(self._text_changed)
        self._notes.setEnabled(False)

        self._project_name = None
        self._step_name = None
        self._version_name = None
        self._filepath = None

        layout = QGridLayout(self)
        layout.addWidget(self._notes)

        self.setMinimumWidth(500)

    def clear(self):
        self._project_name = None
        self._step_name = None
        self._version_name = None
        self._notes.clear()

    def set_entity(self, project_name=None, step_name=None, version_name=None):  # FIXME find a better name
        self._project_name = project_name
        self._step_name = step_name
        self._version_name = version_name

        self._load()
        self._notes.setEnabled(any([self._project_name, self._step_name, self._version_name]))

    def _load(self):
        notes = ""
        if self._version_name is not None and self._step_name is not None and self._project_name is not None:
            notes = VersionAPI.get_notes(self._project_name, self._step_name, self._version_name)

        elif self._project_name is not None and self._step_name is not None:
            notes = StepAPI.get_notes(self._project_name, self._step_name)

        elif self._project_name is not None:
            notes = ProjectAPI.get_notes(self._project_name)

        self._notes.setPlainText(notes)

    def _text_changed(self):
        notes = self._notes.toPlainText()
        if self._version_name is not None and self._step_name is not None and self._project_name is not None:
            VersionAPI.set_notes(self._project_name, self._step_name, self._version_name, notes)

        elif self._project_name is not None and self._step_name is not None:
            StepAPI.set_notes(self._project_name, self._step_name, notes)

        elif self._project_name is not None:
            ProjectAPI.set_notes(self._project_name, notes)
