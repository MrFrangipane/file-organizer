from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QGroupBox, QGridLayout, QLabel, QPlainTextEdit

from fileorganizer.qt_extensions import make_icon_button


class VersionDetails(QGroupBox):  # FIXME find a better name

    copyFilepathClicked = Signal()
    notesChanged = Signal()

    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)

        self.setTitle("Version details")

        self.label_filepath = QLabel()
        self.button_copy_filepath = make_icon_button(
            "Copy filepath to clipboard",
            "clipboard.png",
            self.copyFilepathClicked
        )

        self.notes = QPlainTextEdit()
        self.notes.textChanged.connect(self.notesChanged)
        group_notes = QGroupBox("Notes")
        layout_notes = QGridLayout(group_notes)
        layout_notes.addWidget(self.notes)

        contextual_actions_widget = QWidget()
        self.contextual_actions_layout = QGridLayout(contextual_actions_widget)
        self.contextual_actions_layout.setContentsMargins(0, 0, 0, 0)

        layout = QGridLayout(self)
        layout.addWidget(self.label_filepath, 0, 0)
        layout.addWidget(self.button_copy_filepath, 0, 1)
        layout.addWidget(group_notes, 1, 0, 1, 2)
        layout.addWidget(contextual_actions_widget, 2, 0, 1, 2)
        layout.setColumnStretch(0, 100)
        layout.setRowStretch(1, 100)

    def clear(self):
        self.blockSignals(True)
        self.label_filepath.clear()
        self.notes.clear()
        for i in reversed(range(self.contextual_actions_layout.count())):
            self.contextual_actions_layout.itemAt(i).widget().deleteLater()
        self.add_contextual_action_widget(QLabel("No action available"))
        self.blockSignals(False)

    def set_filepath(self, filepath):
        self.label_filepath.setText(filepath)
        self.label_filepath.setToolTip(filepath)

    def filepath(self):
        return self.label_filepath.text()

    def set_notes(self, notes):
        self.notes.blockSignals(True)
        self.notes.setPlainText(notes)
        self.notes.blockSignals(False)

    def get_notes(self):
        return self.notes.toPlainText()

    def add_contextual_action_widget(self, widget):
        # FIXME
        for i in reversed(range(self.contextual_actions_layout.count())):
            widget_ = self.contextual_actions_layout.itemAt(i).widget()
            if isinstance(widget_, QLabel) and widget_.text() == "No action available":
                widget_.deleteLater()

        self.contextual_actions_layout.addWidget(widget, 0, self.contextual_actions_layout.count())
