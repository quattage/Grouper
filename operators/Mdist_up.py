import bpy
from ..utils.logger import logger


class GROUPER_OT_MDistUp(bpy.types.Operator):
    bl_idname = 'grouper.dist_up'
    bl_label = 'Up'
    bl_description = 'Move the selected object up'



    def execute(self, context):
        mdlist = context.scene.grouper_mdlist
        index = context.scene.grouper_mdlist_index
        index_goal = index - 1
        mdlist.move(index_goal, index)
        bpy.context.scene.grouper_mdlist_index = index_goal
        return {'FINISHED'}


op_class = GROUPER_OT_MDistUp
