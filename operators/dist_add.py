import bpy
from ..utils.logger import logger


class GROUPER_OT_DistAdd(bpy.types.Operator):
    bl_idname = 'grouper.dist_add'
    bl_label = 'Add Distinguisher'
    bl_description = 'Add new enum item'

    new_name: bpy.props.StringProperty(default= 'Preset name', name = 'Preset name ')

    def execute(self, context):
        logger.log("Add Dist", "")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=200)

op_class = GROUPER_OT_DistAdd