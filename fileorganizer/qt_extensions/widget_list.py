from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QGroupBox, QGridLayout, QListWidget, QListWidgetItem

from fileorganizer.qt_extensions import make_icon_button


class WidgetList(QGroupBox):  # FIXME find a better name

    newClicked = Signal()
    documentationClicked = Signal()
    refreshClicked = Signal()
    currentChanged = Signal()
    pathToClipboardClicked = Signal()

    def __init__(self, caption, horizontal=False, parent=None):
        QGroupBox.__init__(self, caption, parent)

        self.caption = caption

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

        self.button_new = make_icon_button(f"Create new {caption}", 'plus.png', self.newClicked)
        self.button_docs = make_icon_button("Open documentation folder", 'file.png', self.documentationClicked)
        self.button_refresh = make_icon_button("Refresh list", 'refresh.png', self.refreshClicked)
        self.button_path_to_clipboard = make_icon_button("Copy path to clipboard", 'clipboard-folder.png', self.pathToClipboardClicked)

        layout = QGridLayout(self)
        layout.addWidget(self.list, 0, 0, 1, 5)

        layout.addWidget(QWidget(), 1, 0)
        layout.addWidget(self.button_new, 1, 1)
        layout.addWidget(self.button_refresh, 1, 2)
        layout.addWidget(self.button_docs, 1, 3)
        layout.addWidget(self.button_path_to_clipboard, 1, 4)

        layout.setColumnStretch(0, 100)

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
        self.blockSignals(False)

    def selected(self):
        index = self.list.currentIndex()
        if index.isValid():
            return self.list.indexWidget(index).name

    def _changed(self):
        self.currentChanged.emit()
