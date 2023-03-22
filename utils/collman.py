import bpy
from bpy.types import Collection
from ..utils.general import stringutils

unresolved_collections = []
moved_collections = []

"""
This class is designed to make it quicker and easier to develop Blender
addons that need to do a lot of managomg moving, and renaming of collections.

The class assumes that your collection instance (made with the create() method)
always exists. For the most part, you should never encounter problems with NoneTypes

With the exception of a few cases, such as grouping hierarchies, (see the link_hierarchy()
method) this class is only designed to handle singular collections at a time. 
"""


def get(name: str) -> Collection:
    """Gets the collection instances that matches the provided name if
    one exists. Will throw an """
    check = is_created(name)
    if check:
        return check
    raise BaseException("A collection called " + name + " was not found!")


def create(name: str, icon_name: str = "OUTLINER_COLLECTION") -> Collection:
    """Creates a new orphan collection and returns it. If a collection
    of this name already exists, that instance will be returned.
    Note: This collection will not be linked to the scene! It must
    be linked for it to show up in the outliner!"""
    check = is_created(name)
    if check:
        unresolved_collections.append(check)
        return check
    coll = bpy.data.collections.new(name)
    
    if icon_name != "OUTLINER_COLLECTION":
        tag = "COLOR" + icon_name[stringutils.find_nth(icon_name, "_", 2):]
        coll.color_tag = tag
        print(tag)
    
    return coll


def destroy(collection: Collection):
    """Permanantly deletes a collection and its members."""
    for obj in collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(collection)


def remove_and_preserve(collection: Collection):
    """Removes a collection and moves its members to the Scene Collection"""
    for obj in collection.objects:
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        bpy.context.scene.collection.objects.link(obj)
    bpy.data.collections.remove(collection)


def move_children(collection: Collection):
    """Moves all of the child objects from the specified collection to the scene collection."""
    for obj in collection.objects:
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        bpy.context.scene.collection.objects.link(obj)
        

def delete_children(collection: Collection):
    """Perminantly deletes all of the child objects from the specified collection."""
    for obj in collection.objects:
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        bpy.context.scene.collection.objects.link(obj)

def move_children_to(from_coll: Collection, to_coll: Collection):
    """Moves all of the child objects from the first collection to the second."""
    for obj in from_coll.objects:
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        to_coll.objects.link(obj)


def rename(collection: Collection, desired_name: str) -> bool:
    """Renames the desired collection. Raises a NameError if the name you choose already exists."""
    if not is_created(desired_name):
        collection.name = desired_name
        return True
    raise NameError("Collection rename failed! A collecton already exists with the name \n'" + desired_name + "\'")


def link(collection: Collection):
    """Links (or moves) a collection to the Scene Collection."""
    if collection:
        unlink(collection)
        bpy.context.scene.collection.children.link(collection)


def unlink(collection: Collection):
    """Unlinks a collection from wherever it may be."""
    if collection:
        if is_linked(collection):
            parent = get_parent(collection)
            if parent:
                parent.children.unlink(collection)
            else:
                bpy.context.scene.collection.children.unlink(collection)


def is_linked(collection: Collection) -> bool:
    """Returns true if the collection is linked anywhere in the scene."""
    if collection:
        check = bpy.context.scene.user_of_id(collection)
        if check:
            return True
        return False


def is_created(collection_name: Collection) -> bool:
    """Returns true if a collection of this name is created anywhere the blend file.
    Does not have to be linked."""
    check = bpy.data.collections.get(collection_name)
    if check:
        return check
    return False


def link_to(coll_child: Collection, coll_parent: Collection):
    """Links a collection to a given parent collection.
    Can be used to move collections."""
    scene_keywords = ["scene", "scene_colleciton", "none"]
    if coll_child and coll_parent:
        unlink(coll_child)
        if coll_parent in scene_keywords:
            link(coll_child)
        else:
            coll_parent.children.link(coll_child)


def link_hierarchy(collections: list):
    """Automatically links a given list of collection instances to each other,
    creating a chain of nested colelctions."""
    if not isinstance(collections, list):
        raise TypeError("Input must be a list.")
    for num, this_coll in enumerate(collections):
        dest_coll = None
        if num != 0:
            dest_coll = collections[num-1]
            link_to(this_coll, dest_coll)
        else:
            link(this_coll)


def get_parent(coll: Collection) -> Collection:
    """Returns the parent of the input collection.
    Returns a NoneType if the input collection belongs to the Scene Collection"""
    all_collections = bpy.data.collections[:]
    parent_collection = next((collection for collection in all_collections if coll.name in collection.children), None)
    if parent_collection:
        return parent_collection
    return None


def clear_errors_list():
    """Clears the ledger of failed/unresolved collections"""
    unresolved_collections.clear()
    moved_collections.clear()


def report_collection_faults(failed_collections: list):
    """Parses the failed_collections and moved_collections lists.
    Automatically generates a message with this info and creates a warning in Blender"""
    if any(isinstance(name, str)for name in failed_collections):
        for count, name in enumerate(failed_collections):
            if name:
                num_names += 1
                collection_names += " \"" + name + "\","
        collection_names = collection_names.rsplit(',', 1)[0]
        bpy.context.self.report({'INFO'}, str(num_names) + " collections already found:" + collection_names)
