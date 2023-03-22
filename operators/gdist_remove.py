import bpy
from ..utils.logger import logger


class GROUPER_OT_MDistRemove(bpy.types.Operator):
    bl_idname = 'grouper.gdist_remove'
    bl_label = 'Remove Collection'
    bl_description = 'Remove a Collection from the list'


    def execute(self, context):
        gdlist = context.scene.grouper_gdlist
        gdlist_index = context.scene.grouper_gdlist_index
        
        if not gdlist_index > len(gdlist):
            if gdlist[gdlist_index]:
                gdlist.remove(gdlist_index)
            else:
                self.report({'WARN'}, "Something went wrong")
        else: 
            self.report({'WARN'}, "Grouper: No active element")
        
        return {'FINISHED'}


op_class = GROUPER_OT_MDistRemove
