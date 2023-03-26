import json
import bpy
from bpy.props import EnumProperty, StringProperty, IntProperty, BoolProperty
from bpy.types import Operator, PropertyGroup
from ..utils.logger import logger
from ..utils.general import proputils, stringutils
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
        mdlist = context.scene.grouper_mdlist
        gdlist = bpy.context.scene.grouper_gdlist
        arguments_list = bpy.context.scene.grouper_custom_args
        active_distinguisher = meshdist.serialize_from_identifier(self.meshdist_types)
        active_distinguisher.destination_name = self.groupdists
        #active_distinguisher.custom_args = 
        
        args = bpy.context.scene.grouper_custom_args
        layout = self.layout
        layout.prop(self, "meshdist_types")
        layout.prop(self, "groupdists")
        
        
        
        display = layout.column()
        
        synop = display.box().row()
        synop.label(icon=active_distinguisher.icon_name, text=active_distinguisher.name)
        synop.label(icon="FORWARD")
        
        gdrow = synop.row()
        
        destname = "(INVLAID)"
        if active_distinguisher.destination_name:
            gdobj = groupdist.get_obj_from_id(gdlist, active_distinguisher.destination_name) 
            if not gdobj:
                gdrow.label(icon="SEQUENCE_COLOR_01", text="INVALID")
            else:
                destname = gdobj.group_name
                gdrow.label(icon=gdobj.icon_name, text=gdobj.group_name)
        else:
            destname = "(NO DESTINATION)"
            gdrow.label(icon="LAYER_USED", text="No Destination")
        
        desc = display.box()
        if active_distinguisher.description:
            stringutils.wrap(active_distinguisher.description + ", move the object to '" + destname + "'", desc, 39)
        else:
            stringutils.wrap("'" + active_distinguisher.name + "' has no description. You may wanna report this.", desc, 39)            
        
        argsettings = layout.column(align=True)
        if len(args) > 0:
            for item in args:
                argument = argsettings.box().row()
                if item.arg_type == "bool":
                    argument.label(text=stringutils.formatkey(item.arg_name))
                    argument.prop(data=item, property="arg_bool", text="")
                elif item.arg_type == "str":
                    argument.label(text=stringutils.formatkey(item.arg_name))
                    argument.prop(data=item, property="arg_str", text="")
                elif item.arg_type == "int":
                    argument.label(text=stringutils.formatkey(item.arg_name))
                    argument.prop(data=item, property="arg_int", text="")
        else:
            argument = argsettings.box().row()
            argument.label(text="No custom args")
            pass


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=230)

op_class = GROUPER_OT_MDistAdd
