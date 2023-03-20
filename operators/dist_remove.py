import bpy
from ..utils.logger import logger


class GROUPER_OT_DistRemove(bpy.types.Operator):
    bl_idname = 'grouper.dist_remove'
    bl_label = 'Remove Distinguisher'
    bl_description = 'Remove a Distinguisher from the ordered list'


    def execute(self, context):
        mdlist = context.scene.grouper_mdlist
        mdlist_index = context.scene.grouper_mdlist_index
        
        if not mdlist_index > len(mdlist):
            if mdlist[mdlist_index]:
                mdlist.remove(mdlist_index)
            else:
                self.report({'WARN'}, "Something went wrong")
        else: 
            self.report({'WARN'}, "Grouper: No active element")
        
        return {'FINISHED'}


op_class = GROUPER_OT_DistRemove
