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
        
        gdlist = context.scene.grouper_gdlist
        
        raw = collman.create("Raw")
        groups = collman.create("Groups")
        collman.link(raw)
        collman.link(groups)
        
        for coll in gdlist:
            ac = collman.create(coll.group_name, coll.icon_name)
            collman.link_to(ac, groups)
        
        return {'FINISHED'}

op_class = GROUPER_OT_GenCollections
