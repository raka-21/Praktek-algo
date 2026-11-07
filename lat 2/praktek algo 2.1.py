
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene,
    QGraphicsView, QAction
)
from PyQt5.QtCore import Qt, QRectF, QEvent
from PyQt5.QtGui import QPen, QBrush, QColor


class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drawing App - Praktik 2.1")
        self.setGeometry(300, 200, 800, 600)

        # Canvas
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 500)

        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Toolbar
        toolbar = self.addToolBar("Tools")

        rect_action = QAction("Rectangle", self)
        ellipse_action = QAction("Ellipse", self)
        line_action = QAction("Line", self)
        clear_action = QAction("Clear", self)

        toolbar.addAction(rect_action)
        toolbar.addAction(ellipse_action)
        toolbar.addAction(line_action)
        toolbar.addAction(clear_action)

        rect_action.triggered.connect(self.add_rectangle)
        ellipse_action.triggered.connect(self.add_ellipse)
        line_action.triggered.connect(self.add_line)
        clear_action.triggered.connect(self.clear_scene)

        # Drawing settings
        self.current_shape = None
        self.start_point = None

        self.view.viewport().installEventFilter(self)

        self.statusBar().showMessage("Pilih bentuk untuk mulai menggambar")

    def add_rectangle(self):
        self.current_shape = "rect"
        self.statusBar().showMessage("Mode: Rectangle")

    def add_ellipse(self):
        self.current_shape = "ellipse"
        self.statusBar().showMessage("Mode: Ellipse")

    def add_line(self):
        self.current_shape = "line"
        self.statusBar().showMessage("Mode: Line")

    def clear_scene(self):
        self.scene.clear()
        self.statusBar().showMessage("Canvas berhasil dibersihkan")

    def eventFilter(self, obj, event):

        if obj == self.view.viewport():

            if event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton and self.current_shape:
                    self.start_point = self.view.mapToScene(event.pos())
                    return True

            elif event.type() == QEvent.MouseButtonRelease:
                if self.start_point is not None:
                    end_point = self.view.mapToScene(event.pos())

                    pen = QPen(Qt.black, 2)
                    brush = QBrush(QColor(100, 150, 200, 100))

                    rect = QRectF(
                        self.start_point,
                        end_point
                    ).normalized()

                    if self.current_shape == "rect":
                        self.scene.addRect(rect, pen, brush)

                    elif self.current_shape == "ellipse":
                        self.scene.addEllipse(rect, pen, brush)

                    elif self.current_shape == "line":
                        self.scene.addLine(
                            self.start_point.x(),
                            self.start_point.y(),
                            end_point.x(),
                            end_point.y(),
                            pen
                        )

                    self.start_point = None
                    return True

        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DrawingApp()
    window.show()
    sys.exit(app.exec_())
