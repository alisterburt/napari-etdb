from magicgui import magicgui

from napari._qt.containers import QtListModel, QtListView
from qtpy.QtGui import QImage
from qtpy.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from qtpy.QtCore import QModelIndex, QSize, Qt
import skimage.io
from skimage.color import gray2rgba
from .browser import Browser
from napari.layers import Image, Points
import numpy as np
from napari.qt.threading import thread_worker


class EntryListModel(QtListModel):
    """Model for QtListView of Micrographs"""
    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        """Return data at `index` for the requested `role`.
        See https://doc.qt.io/qt-5/model-view-programming.html#item-roles
        """
        if role == Qt.DisplayRole:
            entry = index.data(Qt.UserRole)
            return f'{entry.species}'
        if role == Qt.SizeHintRole:
            return QSize(160, 20)
        # if role == Qt.DecorationRole:  # thumbnail image
        #     entry = index.data(Qt.UserRole)
        #     image = gray2rgba(skimage.io.imread(entry.preview_image_url))
        #
        #     return QImage(
        #         thumbnail,
        #         32,
        #         32,
        #         QImage.Format_RGBA8888,
        #     )
        return super().data(index, role)


class EntryListWidget(QtListView):
    """QtListView comes from napari and works with the SelectableEventedist"""
    def __init__(self, root, parent=None):
        super().__init__(root=root, parent=parent)
        self.setModel(EntryListModel(root))
        self.setCurrentIndex(self.selectionModel().currentIndex())


class BrowserWidget(QWidget):
    def __init__(self, viewer: 'Viewer', parent=None):
        super().__init__(parent=parent)

        self.viewer = viewer
        self.browser = Browser()
        self.image_layer = viewer.add_image(np.zeros((28, 28)))
        self.points_layer = viewer.add_points([], face_color='magenta')

        self.entry_list_widget = EntryListWidget(
            self.browser.entries, parent=self
        )
        self.send_to_server_button = QPushButton('send points to server')
        self.entry_info_widget = QLabel('entry info placeholder')

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.entry_list_widget)
        self.layout().addWidget(self.send_to_server_button)
        self.layout().addWidget(self.entry_info_widget)

        self.send_to_server_button.clicked.connect(self.send_to_server)

    def refresh_viewer(self):
        self.viewer.reset_view()
        self.image_layer.reset_contrast_limits_range()
        self.image_layer.reset_contrast_limits()

    def send_to_server(self):
        print(f'points layer data sent to server:\n{self.points_layer.data}')

