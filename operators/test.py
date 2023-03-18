import bpy
from ..utils import collman, objman
from ..utils.logger import logger


class GROUPER_OT_Test(bpy.types.Operator):
    bl_idname = "grouper.test"
    bl_label = "Test Operation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_description = 'Test Operation'
    
    def execute(self, context):
        
        global_mdlist = context.scene.grouper_mdlist
        global_mdlist.clear()
        self.report({"INFO"}, "dists cleared")

        return {"FINISHED"}
    

op_class = GROUPER_OT_Test
