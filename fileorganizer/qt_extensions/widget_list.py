from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QGroupBox, QGridLayout, QListWidget, QListWidgetItem

from fileorganizer.qt_extensions import make_icon_button


class WidgetList(QGroupBox):  # FIXME find a better name

    newClicked = Signal()
    documentationClicked = Signal()
    refreshClicked = Signal()
    currentChanged = Signal()

    def __init__(self, caption, horizontal=False, parent=None):
        QGroupBox.__init__(self, caption, parent)

        self._is_horizontal = horizontal
        self.list = QListWidget()
        self.list.currentItemChanged.connect(self._changed)

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

        layout = QGridLayout(self)
        layout.addWidget(self.list, 0, 0, 1, 4)

        layout.addWidget(QWidget(), 1, 0)
        layout.addWidget(self.button_new, 1, 1)
        layout.addWidget(self.button_refresh, 1, 2)
        layout.addWidget(self.button_docs, 1, 3)

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
        self.list.clear()

    def selected(self):
        index = self.list.currentIndex()
        if index.isValid():
            if self._is_horizontal:
                return self.list.itemWidget(self.list.item(index.column())).name
            else:
                return self.list.itemWidget(self.list.item(index.row())).name

    def _changed(self):
        self.currentChanged.emit()
