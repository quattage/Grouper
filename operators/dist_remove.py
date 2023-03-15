import bpy
from ..utils.logger import logger


class GROUPER_OT_DistRemove(bpy.types.Operator):
    bl_idname = 'grouper.dist_remove'
    bl_label = 'Remove Distinguisher'
    bl_description = 'Remove old enum item'

    new_name: bpy.props.StringProperty(default= 'Preset name', name = 'Preset name ')

    def execute(self, context):
        logger.log("Remove Dist", "")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=200)
    
op_class = GROUPER_OT_DistRemove
