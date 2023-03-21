import bpy
from bpy.props import EnumProperty
from bpy.types import Operator, Panel
from ..utils.logger import logger
from ..distinguishers import meshdist, groupdist

class GROUPER_OT_MDistAdd(Operator):
    bl_idname = 'grouper.dist_add'
    bl_label = 'Add Distinguisher'
    bl_description = 'Add a Distinguisher to the ordered list'
    
    meshdist_types: meshdist.build_enum()
    groupdists: groupdist.build_enum()
    
    def execute(self, context):
        mdlist = context.scene.grouper_mdlist
        gdlist = context.scene.grouper_gdlist
        
        print(mdlist)
        print(gdlist)
        return {'FINISHED'}


#    def draw(self, context):
#       pass

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=200)


op_class = GROUPER_OT_MDistAdd
