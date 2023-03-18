import json
import bpy
from ..utils import collman
from ..utils.logger import logger
from ..distinguishers import meshdist

class GROUPER_OT_RegisterDefaults(bpy.types.Operator):
    bl_idname = "grouper.register_defaults"
    bl_label = "Register Defaults"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_description = 'Registers a set of default Mesh and Group distinguishers'

    def execute(self, context):
        deflist = meshdist.get_defaults()
        global_mdlist = context.scene.grouper_mdlist
        
        if not global_mdlist:
            logger.log("Registering Default Distinguishers...", "")
            for entry in deflist:
                mdlist = global_mdlist.add()
                mdlist.name = entry.name
                mdlist.identifier = entry.identifier
                mdlist.icon_name = entry.icon_name
                mdlist.custom_args = json.dumps(entry.custom_args)
                mdlist.destination_name = entry.destination_name
                
        
        return {'FINISHED'}

op_class = GROUPER_OT_RegisterDefaults