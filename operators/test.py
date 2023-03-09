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
        
        objects = objman.get_children(collman.get("High"))
        objman.move(objects, collman.get("Low"))

        return {"FINISHED"}
    

op_class = GROUPER_OT_Test
