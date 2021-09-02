from napari_etdb.gui import BrowserWidget
from napari.qt.threading import thread_worker
import napari

viewer = napari.Viewer()
browser_widget = BrowserWidget(viewer)
viewer.window.add_dock_widget(
    browser_widget, area='right', name='ETDB browser'
)


def on_preview_image_received(new_image):
    browser_widget.points_layer.data = []
    browser_widget.image_layer.data = new_image
    browser_widget.refresh_viewer()


@thread_worker(connect={"yielded": on_preview_image_received})
def fetch_preview_image_async(event=None):
    while True:
        yield browser_widget.browser.fetch_preview_image()


browser_widget.browser.entries.selection.events.active.connect(
    fetch_preview_image_async
)



