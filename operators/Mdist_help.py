import bpy
from ..utils.logger import logger


class GROUPER_OT_MDistHelp(bpy.types.Operator):
    bl_idname = 'grouper.dist_help'
    bl_label = 'Help'
    bl_description = 'Display a help dialogue in the Details panel'
    def execute(self, context):
        context.scene.grouper_mdlist_index = len(context.scene.grouper_mdlist)
        return {'FINISHED'}

op_class = GROUPER_OT_MDistHelp
