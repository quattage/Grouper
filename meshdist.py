import bpy
import abc
from bpy.types import Object


def hasModifier(obj, name: str) -> bool:
    return True if name in obj.modifiers else False
        

class Distinguisher(abc.ABC):
    name = ""
    identifier = ""
    used = False
    
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def isfulfilled(obj: object = None) -> bool:
        return False

    def get_custom_args():
        pass
    

# DISTINGUISHERS
class MD_Midpoint(Distinguisher):
    def __init__(self):
        self.name = "Midpoint"
        self.identifier = __class__.__name__

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_UVSets(Distinguisher):
    def __init__(self):
        self.name = "UVs"
        self.identifier = __class__.__name__

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_Subdivision(Distinguisher):
    def __init__(self):
        self.name = "Subdivisions"
        self.identifier = __class__.__name__

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_Bevel(Distinguisher):
    def __init__(self):
        self.name = "Bevel"
        self.identifier = __class__.__name__

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_WeightedNormal(Distinguisher):
    def __init__(self):
        self.name = "Weighted Normals"
        self.identifier = __class__.__name__

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False


class MD_SmoothGroups(Distinguisher):
    def __init__(self):
        self.name = "Smooth Groups"
        self.identifier = __class__.__name__

    def isfulfilled(self, obj: object = None) -> bool:
        if not isinstance(obj, Object):
            raise BaseException(self.name + " only accepts instances of objects!")
        return False
# DISTINGUISHERS


distlist = (
    MD_Midpoint(),
    MD_UVSets(),
    MD_Subdivision(),
    MD_Bevel(),
    MD_WeightedNormal(),
    MD_SmoothGroups(),
)


def get_distinguishers() -> dict:
    distinguishers = {}
    for md in distlist:
        distinguishers.update({md.identifier: md})
    return distinguishers

