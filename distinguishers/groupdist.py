

import bpy
import re
from .. import preferences
from bpy.props import EnumProperty

from bpy.types import Object
from ..utils.logger import logger

def hasModifier(obj, name: str) -> bool:
    return True if name in obj.modifiers else False


class CollectionDistinguisher():
    group_name = ""
    suffix_name = ""
    identifier = ""
    icon_name = ""
    export_settings = {}
    

    def __init__(self, group_name: str = None, suffix_name: str = None, color: int | str = 0, export_settings: dict = preferences.get_export_defaults()):
        if not(isinstance(group_name, str) or isinstance(suffix_name, str)):
            raise BaseException("Collection Distinguisher was initialized incorrectly!")
        if isinstance(color, int):
            if not (color > 0 and color < 9):
                raise BaseException("Collection 'color' if passed int must be between 0 and 8!")
        elif not isinstance(color, str):
            raise TypeError("Collection Distinguisher 'color' property expects an int or string!")

        suffix_name = re.sub(r'\W+', '', re.sub("_", '', suffix_name))
        group_name = re.sub(r'\W+', '', group_name)
        
        if isinstance(color, int):
            if color == 0:
                self.icon_name = "OUTLINER_COLLECTION"
            else:
                self.icon_name = "COLLECTION_COLOR_0" + str(color) 
        else:
            self.icon_name = color
        if suffix_name:
            if suffix_name[0] != "_":
                suffix_name = "_" + suffix_name
        else:
            suffix_name = ""
            
        self.group_name = group_name
        self.suffix_name = suffix_name
        self.identifier = self.group_name
        if export_settings:
            self.export_settings = str(export_settings)
        else:
            self.export_settings = ""


def get_defaults() -> list:
    distlist = [
        CollectionDistinguisher("Highpoly", "_high", 5),
        CollectionDistinguisher("Lowpoly", "_low", 5),
        CollectionDistinguisher("Unresolved", "", 2, False)
    ]
    return distlist


def serialize(pgitem) -> CollectionDistinguisher:
    """Creates a new Distinguisher object based on data from an input PropertyGroup"""
    if pgitem is None:
        raise TypeError("Serializer was passed a NoneType!")
    if isinstance(pgitem, CollectionDistinguisher):         # Instantiate a CollectionDistinguisher
        group_name = pgitem.group_name
        suffix_name = pgitem.suffix_name
        icon_name = pgitem.icon_name
        instance = CollectionDistinguisher(group_name, suffix_name, icon_name)
        return instance
    else:
        raise TypeError("'" + type(pgitem).__name__ + "' was passed to serializer, expected a CollectionDistinguisher")


def register_group(group_name, suffix_name, icon_name, context):
    new_item = context.scene.grouper_gdlist.add()
    new_item.group_name = group_name
    new_item.suffix_name = suffix_name
    new_item.icon_name = icon_name
    new_item.identifier = "GD_" + group_name + ":" + suffix_name
    return new_item


def get_colls_as_enum_entries(self, context) -> list:
    colls = bpy.context.scene.grouper_gdlist
    itemlist = []
    for ind, entry in enumerate(colls):
        enumentry = (entry.identifier, entry.group_name, "Collection to add grouped items to", entry.icon_name, ind)
        itemlist.append(enumentry)
    return itemlist


def get_obj_from_name(dlist, name):
    for obj in dlist:
        if obj.group_name == name:
            return obj
    return None


def get_obj_from_id(dlist, identifier):    
    for obj in dlist:
        if obj.identifier == identifier:
            return obj
    return None


def build_enum() -> EnumProperty:
    return EnumProperty(items=get_colls_as_enum_entries, name="")
