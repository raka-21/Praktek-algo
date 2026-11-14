import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class SourceListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            mimeData = QMimeData()
            mimeData.setText(item.text())
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.CopyAction)

class TargetListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.source() == self:
            super().dropEvent(event)
        elif event.mimeData().hasText():
            self.addItem(event.mimeData().text())
            event.acceptProposedAction()

class DragDropApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Demo")
        self.setGeometry(300, 300, 650, 450)

        main_layout = QHBoxLayout()

        # Left Panel (Source)
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Source (drag from here):"))
        self.source_list = SourceListWidget()
        self.source_list.addItems(["Apple", "Banana", "Cherry", "Date", "Elderberry"])
        left_layout.addWidget(self.source_list)

        # Right Panel (Target)
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Target (drop here):"))
        self.target_list = TargetListWidget()
        self.clear_btn = QPushButton("Clear Target")
        self.clear_btn.clicked.connect(self.target_list.clear)
        right_layout.addWidget(self.target_list)
        right_layout.addWidget(self.clear_btn)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DragDropApp()
    window.show()
    sys.exit(app.exec_())