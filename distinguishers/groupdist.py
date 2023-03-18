

import bpy
import json, re

from bpy.types import Object
from ..utils.logger import logger

def hasModifier(obj, name: str) -> bool:
    return True if name in obj.modifiers else False


class Grouper():
    group_name = None
    suffix_name = None

    def __init__(self, group_name: str = None, suffix_name: str = None):
        if not(isinstance(group_name, str) or isinstance(suffix_name, str)):
            raise BaseException("Grouper object was initialized incorrectly!")

        suffix_name = re.sub(r'\W+', '', re.sub("_", '', suffix_name))
        group_name = re.sub(r'\W+', '', group_name)

        if suffix_name[0] != "_":
            suffix_name = "_" + suffix_name
            logger.log("Grouper object suffix was initialized without a _", "WARNING")

        self.group_name = group_name
        self.suffix_name = suffix_name


def get_defaults() -> list:
    distlist = [
        Grouper("Highpoly", "_high"),
        Grouper("Lowpoly", "_low")
    ]
    return distlist
