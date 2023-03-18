import bpy
from ..utils.logger import logger


class GROUPER_OT_DistRemove(bpy.types.Operator):
    bl_idname = 'grouper.dist_remove'
    bl_label = 'Remove Distinguisher'
    bl_description = 'Remove old enum item'

    global to_remove
    to_remove = ""
    
    use_low: bpy.props.BoolProperty(default=False, name = "Change Low")

    def execute(self, context):
        logger.log("Remove Dist", "")
        return {'FINISHED'}


op_class = GROUPER_OT_DistRemove
