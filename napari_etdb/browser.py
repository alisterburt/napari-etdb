import numpy as np
from napari import Viewer
import skimage.io


from .etdb import get_entries


class Browser:
    def __init__(self):
        self.entries = get_entries()

    @property
    def current_entry(self):
        return self.entries.selection._current

    def fetch_preview_image(self):
        return skimage.io.imread(self.current_entry.preview_image_url)






