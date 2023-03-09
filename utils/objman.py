import bpy
from bpy.types import Collection
from bpy.types import Object
from .collman import *

moved_objects = []

"""
Similar to the collman class, this class is designed to move, group, and rename objects.
Most of the methods here are designed to accept both singular object instances, as well
as lists of objects. 

This class assumes that any object you pass each method actually exists, since they had 
to be retrieved from the outliner anyway.
"""


def get(name: str) -> Object:
    """Returns an object that matches the provided name. Will return a 
    NoneType if the object does not exist."""
    obj = bpy.objects.get(name)
    if obj:
        return obj
    return None


def get_children(collection: Collection) -> list:
    """Returns the set of objects contained within the specified collection"""
    output = []
    for obj in collection.objects:
        output.append(obj)
    return output


def get_selection(with_active = True) -> list:
    selection = bpy.context.selected_objects
    active = bpy.context.active_object
    if with_active:
        return selection
    selection.remove(active)
    return selection


def delete(this_object: Object | list):
    """Permanantly deletes an object or list of objects."""
    if isinstance(this_object, list):
        for obj in this_object:
            bpy.data.objects.remove(obj)
    else:
        bpy.data.objects.remove(this_object)


def rename(this_object: Object | list, desired_name: str):
    """Rename the desired object or list of objects. 
    Raises a NameError if the name you choose already exists."""
    if isinstance(this_object, list):
        for obj in this_object:
            if not exists(desired_name):
                this_object.name = desired_name
            else:
                raise NameError("Object rename failed! An object already exists with the name \n'" + desired_name + "\'")
    else:
        if not exists(desired_name):
            this_object.name = desired_name
        else:
            raise NameError("Object rename failed! An object already exists with the name \n'" + desired_name + "\'")


def link(obj: Object, coll_parent: Collection = None):
    """Links (or moves) an object to the destination collection.
    If no destination is specified, the specified object will
    be moved to the Scene Collection."""
    unlink(obj)
    if not coll_parent:
        bpy.context.scene.collection.objects.link(obj)
    else:
        coll_parent.objects.link(obj)


def unlink(obj: Object):
    """Unlinks an object from the scene."""
    parent = get_parent_collection(obj)
    if parent:
        parent.objects.unlink(obj)
    else:
        print("PENIS:  " + str(parent))
        bpy.context.scene.collection.objects.unlink(obj)


def ismesh(this_object: Object | list):
    """If this object is a mesh, returns true
    If every object in the input list is a mesh, return true"""
    if isinstance(this_object, list):
        for obj in this_object:
            if (obj.type != "MESH"):
                return False
        return True
    else:
        return this_object.type == "MESH"


def exists(object_name: str) -> bool:
    """Returns true if an object of this name is present anywhere in the scene."""
    created = bpy.data.objects.get(object_name)
    if created:
        linked = bpy.context.scene.user_of_id(created)
        if linked:
            return created
    return False


def move(objs: Object | list, coll_parent: Collection = None):
    """Moves an object or list of objects to the desired collection.
    If the parent destination is not specified, the object will be
    moved to the Scene collection."""
    if isinstance(objs, list):
        for obj in objs:
            link(obj, coll_parent)
    else:
        link(objs, coll_parent)


def get_parent_collection(obj: Object) -> Collection:
    """Returns the parent collection of the input object.
    Returns a NoneType if the input object is under the Scene Collection"""
    all_collections = bpy.data.collections[:]
    parent_collection = next((collection for collection in all_collections if obj.name in collection.objects), None)
    if parent_collection:
        return parent_collection
    return None


def clear_moves():
    """Clears the ledger of moved objects"""
    moved_objects.clear()
