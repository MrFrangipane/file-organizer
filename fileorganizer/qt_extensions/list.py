from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QGroupBox, QGridLayout, QListWidget, QListWidgetItem

from fileorganizer.qt_extensions import make_icon_button
from fileorganizer.qt_extensions.list_item import ListItem


class List(QGroupBox):

    newClicked = Signal()
    refreshClicked = Signal()
    currentChanged = Signal()

    def __init__(self, caption, parent=None):
        QGroupBox.__init__(self, caption, parent)

        self.list = QListWidget()
        selection_model = self.list.selectionModel()
        selection_model.selectionChanged.connect(self._changed)

        self.list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.list.setAlternatingRowColors(True)

        self.button_new = make_icon_button(
            f"Create new {caption}", 'plus.png',
            self.newClicked,
            caption="New"
        )
        self.button_refresh = make_icon_button(
            "Refresh list", 'refresh.png',
            self.refreshClicked,
            caption="Refresh"
        )

        layout = QGridLayout(self)
        layout.addWidget(self.list, 0, 0, 1, 2)
        layout.addWidget(self.button_new, 1, 0)
        layout.addWidget(self.button_refresh, 1, 1)

    def addItem(self, item: ListItem):
        self.blockSignals(True)
        item_ = QListWidgetItem()
        item_.setSizeHint(item.sizeHint())

        self.list.addItem(item_)
        self.list.setItemWidget(item_, item)

        self.blockSignals(False)

    def clear(self):
        # FIXME dont over update everything
        self.list.clear()

    def selected(self):
        indexes = self.list.selectedIndexes()
        if indexes:
            return self.list.indexWidget(indexes[0]).name

    def _changed(self):
        self.currentChanged.emit()
