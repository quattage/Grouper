import bpy
from ..utils.logger import logger


class GROUPER_OT_GDistDown(bpy.types.Operator):
    bl_idname = 'grouper.gdist_down'
    bl_label = 'Down'
    bl_description = 'Move the selected object down'

    def execute(self, context):
        gdlist = context.scene.grouper_gdlist
        index = context.scene.grouper_gdlist_index
        index_goal = index + 1
        gdlist.move(index_goal, index)
        bpy.context.scene.grouper_gdlist_index = index_goal
        return {'FINISHED'}


op_class = GROUPER_OT_GDistDown
