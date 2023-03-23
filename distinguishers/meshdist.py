

import sys, inspect
import bpy
import json, abc

from bpy.types import EnumProperty, Object
from bpy_types import PropertyGroup
from ..preferences import GROUPER_PT_MDList, GROUPER_PT_GDList
from ..utils.logger import logger

def hasModifier(obj, name: str) -> bool:
    return True if name in obj.modifiers else False


class Distinguisher(abc.ABC):
    name = ""
    identifier = ""
    icon_name = ""
    custom_args = {}
    condition = True
    destination_name = ""
    description = ""

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def isfulfilled(obj: object = None) -> bool:
        return False

    def set_custom_props(props: list = None):
        pass


# DISTINGUISHERS
class MD_Midpoint(Distinguisher):
    def __init__(self, custom_args: dict = {"above_or_below": False}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Midpoint"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = "UGLYPACKAGE"

        if custom_args["above_or_below"]:
            self.description = "If the object's polycount is above " + "TEMP"
        else:
            self.description = "If the object's polycount is below " + "TEMP"

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_UVSets(Distinguisher):
    def __init__(self, custom_args: dict = {"map_name": "UVMap"}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "UVs"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = "GROUP_UVS"
        self.description = "If the object has a UV map called " + custom_args["map_name"]

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_Subdivision(Distinguisher):
    def __init__(self, custom_args: dict = {"levels": 1}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Subdivisions"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = "MOD_SMOOTH"

        levels = custom_args["levels"]
        if levels > 0:
            self.description = "If the object has at least " + str(levels) + " Sub-D levels"
        elif levels == 0:
            self.description = "If the object has a Sub-D modifier"
        elif levels < 0:
            self.description = "If the object has exactly " + str(levels) + " Sub-D levels"

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_Bevel(Distinguisher):
    def __init__(self, custom_args: dict = {"segments": 1}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Bevel"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = "MOD_BEVEL"

        levels = custom_args["segments"]
        if levels > 0:
            self.description = "If the object has at least " + str(levels) + " Bevel levels"
        elif levels == 0:
            self.description = "If the object has a Bevel modifier"
        elif levels < 0:
            self.description = "If the object has exactly " + str(levels) + " Bevel levels"
        self.description = ""

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_WeightedNormal(Distinguisher):
    def __init__(self, custom_args: dict = {"weight": 50}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Weighted Normals"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = "MOD_NORMALEDIT"

        levels = custom_args["weight"]
        if levels > 0:
            self.description = "If the object has Weighted Normals of at least " + str(levels) + " strength"
        elif levels == 0:
            self.description = "If the object has a Weighted Normals modifier "
        elif levels < 0:
            self.description = "If the object has Weighted Normals of exactly " + str(levels) + " strength"
        self.description = ""
        self.description = ""

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_SmoothGroups(Distinguisher):
    def __init__(self, custom_args: dict = {}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Smooth Groups"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = "UGLYPACKAGE"
        self.description = "If the object has any sharps or custom normal information"

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_Keyword(Distinguisher):
    def __init__(self, custom_args: dict = {"word": "Cube", "exact_match": False}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Keyword"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = "OUTLINER_OB_FONT"

        exact = custom_args["exact_match"]
        name = custom_args["word"]

        if exact:
            self.description = "If the object's name is '" + name + "'"
        else:
            self.description = "If the object's name contains the keyword '" + name + "'"

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False
    
class MD_Mesh(Distinguisher):
    def __init__(self, custom_args: dict = {}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Mesh Objects"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = "MESH_CUBE"
        self.description = "If the object is a mesh object"

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False
# DISTINGUISHERS


def get_defaults() -> dict:
    distlist = [
        MD_Keyword({"word": "_high", "exact_match": False}, True, "Highpoly"),
        MD_Bevel({"segments": 1}, True, "Highpoly"),
        MD_Subdivision({"levels": 1}, True, "Highpoly"),
        MD_Mesh({}, True, "Unresolved"),
    ]
    return distlist


def serialize(pgitem) -> dict:
    """Creates a new Distinguisher object based on data from an input PropertyGroup"""
    if pgitem is None:
        raise TypeError("Serializer was passed a NoneType!")
    if isinstance(pgitem, GROUPER_PT_MDList):         # Instantiate a Mesh Distinguisher
        name = pgitem.name
        identifier = pgitem.identifier
        custom_args = json.loads(pgitem.custom_args)
        condition = pgitem.condition
        destination_name = pgitem.destination_name
        distinguisher = getattr(sys.modules[__name__], identifier)
        instance = distinguisher(custom_args, condition, destination_name)
        return instance
    else: 
        raise TypeError("'" + type(pgitem).__name__ + "' was passed to serializer, expected an MDList PropertyGroup!")


def build_enum() -> EnumProperty:
    distinguishers = []
    itemlist = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if isinstance(obj, type(Distinguisher)) and "MD_" in name:
                distinguishers.append(obj)
    for ind, entry in enumerate(distinguishers):
        if ind == 0:
            defid = entry.identifier
        enumentry = (entry().identifier, entry().name, "Distinguisher to group items", entry().icon_name, ind)
        itemlist.append(enumentry)
    return bpy.props.EnumProperty(items=itemlist, name="Type:")

