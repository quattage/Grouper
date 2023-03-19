import bpy
from ..utils import collman
from ..utils.logger import logger

class GROUPER_OT_GenCollections(bpy.types.Operator):
    bl_idname = "grouper.gen_collections"
    bl_label = "Generate Collections"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_description = 'Generates a set of collections for you'

    def execute(self, context):
        logger.log("Generating Collections", "")
        props = bpy.context.scene.grouper_prefs
        
        raw = collman.create("Raw")
        unresolved = collman.create("Unresolved")
        bake_groups = collman.create("Bake Groups")
        group_1 = collman.create("Group_1")
        low = collman.create(props.low_collection_name + "_1")
        high = collman.create(props.high_collection_name + "_1")
        collman.link(raw)
        collman.link_hierarchy([bake_groups, group_1, high])
        collman.link_to(low, group_1)
        collman.link_to(unresolved, bake_groups)
        
        
        
        return {'FINISHED'}

op_class = GROUPER_OT_GenCollections
