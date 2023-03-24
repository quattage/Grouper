import bpy
from bpy.props import EnumProperty
from bpy.types import Operator, Panel
from ..utils.logger import logger
from ..utils.general import listutils, stringutils
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
        return {'FINISHED'}


    def draw(self, context):
        gdlist = context.scene.grouper_gdlist
        dist = meshdist.serialize_from_identifier(self.meshdist_types)
        dist.destination_name = self.groupdists
        
        layout = self.layout
        layout.prop(self, "meshdist_types")
        layout.prop(self, "groupdists")
        display = layout.column()
        
        synop = display.box().row()
        synop.label(icon=dist.icon_name, text=dist.name)
        synop.label(icon="FORWARD")
        
        gdrow = synop.row()
        
        destname = "(INVLAID)"
        if dist.destination_name:
            gdobj = groupdist.get_obj_from_id(gdlist, dist.destination_name) 
            if not gdobj:
                gdrow.label(icon="SEQUENCE_COLOR_01", text="INVALID")
            else:
                destname = gdobj.group_name
                gdrow.label(icon=gdobj.icon_name, text=gdobj.group_name)
        else:
            destname = "(NO DESTINATION)"
            gdrow.label(icon="LAYER_USED", text="No Destination")
        
        desc = display.box()
        if dist.description:
            stringutils.wrap(dist.description + ", move the object to '" + destname + "'", desc, 39)
        else:
            stringutils.wrap("'" + dist.name + "' has no description. You may wanna report this.", desc, 39)
        
        
        argsview = display.column(align=True)
        if dist.custom_args:
            for key, value in dist.custom_args.items():
                arg = argsview.box().row(align=True)
                arg.label(icon="KEYFRAME", text=stringutils.formatkey(key))
        else:
            arg = argsview.box().row(align=True)
            arg.label(icon="FILE_BLANK", text="No additional arguments")
            

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=230)



op_class = GROUPER_OT_MDistAdd
