import json
import bpy
from ..utils import collman
from ..utils.logger import logger
from ..distinguishers import meshdist, groupdist

class GROUPER_OT_RegisterDefaults(bpy.types.Operator):
    bl_idname = "grouper.register_defaults"
    bl_label = "Register Defaults"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_description = 'Registers a set of default Mesh and Group distinguishers'

    def execute(self, context):
        
        global_mdlist = context.scene.grouper_mdlist
        global_gdlist = context.scene.grouper_gdlist
        
        deflist = meshdist.get_defaults()
        if not global_mdlist:
            logger.log("Registering Default Distinguishers...", "")
            for entry in deflist:
                mdlist = global_mdlist.add()
                mdlist.name = entry.name
                mdlist.identifier = entry.identifier
                mdlist.condition = entry.condition
                mdlist.icon_name = entry.icon_name
                mdlist.custom_args = json.dumps(entry.custom_args)
                mdlist.destination_name = entry.destination_name
                mdlist.description = entry.description
                
        deflist = groupdist.get_defaults()
        if not global_gdlist:
            for entry in deflist:
                gdlist = global_gdlist.add()
                gdlist.group_name = entry.group_name
                gdlist.identifier = entry.identifier
                gdlist.suffix_name = entry.suffix_name
                gdlist.icon_name = entry.icon_name
                gdlist.for_export = entry.for_export
                
        
        return {'FINISHED'}

op_class = GROUPER_OT_RegisterDefaults