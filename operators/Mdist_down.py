import bpy
from ..utils.logger import logger


class GROUPER_OT_MDistDown(bpy.types.Operator):
    bl_idname = 'grouper.dist_down'
    bl_label = 'Down'
    bl_description = 'Move the selected object down'

    def execute(self, context):
        mdlist = context.scene.grouper_mdlist
        index = context.scene.grouper_mdlist_index
        index_goal = index + 1
        mdlist.move(index_goal, index)
        bpy.context.scene.grouper_mdlist_index = index_goal
        return {'FINISHED'}


op_class = GROUPER_OT_MDistDown
