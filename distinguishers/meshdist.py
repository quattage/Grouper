

import bpy
import json, abc

from bpy.types import Object
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
    def __init__(self, icon_name: str = "UGLYPACKAGE", custom_args: dict = {"above_or_below": False}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Midpoint"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = icon_name

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_UVSets(Distinguisher):
    def __init__(self, icon_name: str = "UGLYPACKAGE", custom_args: dict = {"map_name": "UVMap"}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "UVs"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = icon_name

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_Subdivision(Distinguisher):
    def __init__(self, icon_name: str = "UGLYPACKAGE", custom_args: dict = {"levels": 1}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Subdivisions"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = icon_name

    def isfulfilled(self, icon_name: str = "UGLYPACKAGE", obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_Bevel(Distinguisher):
    def __init__(self, icon_name: str = "UGLYPACKAGE", custom_args: dict = {"segments": 1}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Bevel"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = icon_name

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_WeightedNormal(Distinguisher):
    def __init__(self, icon_name: str = "UGLYPACKAGE", custom_args: dict = {"weight": 50}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Weighted Normals"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = icon_name

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_SmoothGroups(Distinguisher):
    def __init__(self, icon_name: str = "UGLYPACKAGE", custom_args: dict = {}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Smooth Groups"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = icon_name

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False
    
class MD_Keyword(Distinguisher):
    def __init__(self, icon_name: str = "UGLYPACKAGE", custom_args: dict = {"word": "Cube", "exact_match": False}, condition: bool = True, destination_name: str = ""):
        self.custom_args = custom_args
        self.name = "Keyword"
        self.identifier = __class__.__name__
        self.condition = condition
        self.destination_name = destination_name
        self.icon_name = icon_name

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False
# DISTINGUISHERS


def get_defaults() -> dict:
    distlist = [
        MD_Keyword("UGLYPACKAGE", {"word": "_high", "exact_match": False}, True, "Highpoly"),
        MD_Subdivision("UGLYPACKAGE", {"levels": 1}, True, "Highpoly")
    ]
    return distlist
