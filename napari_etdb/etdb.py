"""
Placeholder file for an actual interface to the ETDB
"""

from pydantic import BaseModel
from napari.utils.events import SelectableEventedList
from datetime import date, datetime
from typing import Optional
from .etdb_entries.placeholders import starfish, spheres


class Entry(BaseModel):
    date: Optional[date] = None
    microscopist: Optional[str] = None
    species: Optional[str] = None
    strain: Optional[str] = None
    acquisition_settings: Optional[str] = None
    microscope: Optional[str] = None
    acquisition_software: Optional[str] = None
    processing_software: Optional[str] = None
    notes: Optional[str] = None
    open_index_protocol_id: Optional[str] = None
    preview_image_url: Optional[str] = None
    tomogram_url: Optional[str] = None

    def __hash__(self):
        """Implemented as object in SelectableEventedList must be hashable
        """
        return id(self)


starfish = Entry.parse_obj(starfish)
spheres = Entry.parse_obj(spheres)


def get_entries():
    return SelectableEventedList([starfish, spheres])