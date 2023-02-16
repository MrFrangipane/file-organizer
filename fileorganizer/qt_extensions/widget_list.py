from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QGroupBox, QGridLayout, QListWidget, QListWidgetItem, QSizePolicy

from fileorganizer.qt_extensions import make_icon_button


class WidgetList(QGroupBox):  # FIXME find a better name

    newClicked = Signal()
    openFolderClicked = Signal()
    refreshClicked = Signal()
    currentChanged = Signal()
    pathToClipboardClicked = Signal()

    def __init__(self, caption, widget_size=None, horizontal=False, parent=None):
        QGroupBox.__init__(self, caption, parent)

        self._is_horizontal = horizontal
        self.list = QListWidget()
        selection_model = self.list.selectionModel()
        selection_model.selectionChanged.connect(self._changed)

        if horizontal:
            self.list.setHorizontalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
            self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            self.list.setFlow(QListWidget.LeftToRight)

        else:
            self.list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
            self.list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.list.setAlternatingRowColors(True)

        self.button_new = make_icon_button(
            f"Create new {caption}", 'plus.png',
            self.newClicked,
            caption="New"
        )
        self.button_open_folder = make_icon_button(
            "Open folder in file explorer", 'folder.png',
            self.openFolderClicked,
            caption="Open folder"
        )
        self.button_refresh = make_icon_button(
            "Refresh list", 'refresh.png',
            self.refreshClicked,
            caption="Refresh"
        )
        self.button_path_to_clipboard = make_icon_button(
            "Copy path to clipboard", 'clipboard-folder.png',
            self.pathToClipboardClicked,
            caption="Copy path"
        )

        layout = QGridLayout(self)

        if self._is_horizontal:
            layout.addWidget(self.list, 0, 0, 1, 5)
            layout.addWidget(QWidget(), 1, 0)
            layout.addWidget(self.button_new, 1, 1)
            layout.addWidget(self.button_refresh, 1, 2)
            layout.addWidget(self.button_open_folder, 1, 3)
            layout.addWidget(self.button_path_to_clipboard, 1, 4)
            layout.setColumnStretch(0, 100)
            if widget_size is not None:
                self.list.setFixedHeight(widget_size + self.list.horizontalScrollBar().height())
        else:
            layout.addWidget(self.list, 0, 0, 1, 2)
            layout.addWidget(self.button_new, 1, 0, 1, 2)
            layout.addWidget(self.button_refresh, 2, 0, 1, 2)
            layout.addWidget(self.button_open_folder, 3, 0)
            layout.addWidget(self.button_path_to_clipboard, 3, 1)
            if widget_size is not None:
                self.list.setFixedWidth(widget_size + self.list.verticalScrollBar().width())

        self._update_enabled()

    def addWidget(self, widget):
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())

        self.list.addItem(item)
        self.list.setItemWidget(item, widget)

        if self._is_horizontal:
            self.list.setFixedHeight(widget.sizeHint().height() + self.list.horizontalScrollBar().height())
        else:
            self.list.setFixedWidth(widget.sizeHint().width() + self.list.verticalScrollBar().width())

    def clear(self):
        self.blockSignals(True)
        self.list.clear()
        self._update_enabled()
        self.blockSignals(False)

    def selected(self):
        indexes = self.list.selectedIndexes()
        if indexes:
            return self.list.indexWidget(indexes[0]).name

    def _changed(self):
        self._update_enabled()
        self.currentChanged.emit()

    def _update_enabled(self):
        is_enabled = self.selected() is not None
        self.button_open_folder.setEnabled(is_enabled)
        self.button_path_to_clipboard.setEnabled(is_enabled)
