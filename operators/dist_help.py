import bpy
from ..utils.logger import logger


class GROUPER_OT_DistHelp(bpy.types.Operator):
    bl_idname = 'grouper.dist_help'
    bl_label = 'Help'
    bl_description = 'Deselects all distinguishers so that the Help menu will display'

    use_low = bpy.props.BoolProperty(default=False, name = "Change Low")
    

    def execute(self, context):
        
        
        mdlist = context.scene.grouper_mdlist
        active_mdlist = context.scene.grouper_mdlist_index
        
        logger.log("Help " + str(active_mdlist))
        
        active_mdlist = len(mdlist)
        
        logger.log("After " + str(active_mdlist))
        return {'FINISHED'}

op_class = GROUPER_OT_DistHelp
