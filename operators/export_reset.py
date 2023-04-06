import bpy
from ..utils.logger import logger

class GROUPER_OT_ExportGroups(bpy.types.Operator):
    bl_idname = "grouper.export_reset"
    bl_label = "Re-route"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_description = "Sets Grouper's export location to the location of the .blend file"

    def execute(self, context):
        if not bpy.context.scene.grouper_prefs.export_path:
            bpy.context.scene.grouper_prefs.export_path = bpy.path.abspath("//")
        else:
            members = bpy.context.scene.grouper_prefs.export_path.split("\\")
            destination = members[len(members) - 1]
            bpy.context.scene.grouper_prefs.export_path = bpy.path.abspath("//") + destination
        return {"FINISHED"}
    

op_class = GROUPER_OT_ExportGroups