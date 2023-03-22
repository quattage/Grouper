import bpy


class GROUPER_OT_GDistUp(bpy.types.Operator):
    bl_idname = 'grouper.gdist_up'
    bl_label = 'Up'
    bl_description = 'Move the selected object up'

    def execute(self, context):
        gdlist = context.scene.grouper_gdlist
        index = context.scene.grouper_gdlist_index
        index_goal = index - 1
        gdlist.move(index_goal, index)
        bpy.context.scene.grouper_gdlist_index = index_goal
        return {'FINISHED'}


op_class = GROUPER_OT_GDistUp
