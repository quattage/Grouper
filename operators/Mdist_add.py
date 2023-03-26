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
    
    active_arguments = None
    
    
    def execute(self, context):
        mdlist = context.scene.grouper_mdlist
        gdlist = context.scene.grouper_gdlist
        
        
        return {'FINISHED'}


    def modal(self, context, event):
        mdlist = context.scene.grouper_mdlist
        gdlist = bpy.context.scene.grouper_gdlist
        active_distinguisher =  meshdist.serialize_from_identifier(self.meshdist_types)
        arguments_list = bpy.context.scene.grouper_custom_args
        
        
        proputils.populate_args_instance(context, active_distinguisher.custom_args)
        print("AA", arguments_list)


    def draw(self, context):
        mdlist = context.scene.grouper_mdlist
        gdlist = bpy.context.scene.grouper_gdlist
        active_distinguisher = meshdist.serialize_from_identifier(self.meshdist_types)
        arguments_list = bpy.context.scene.grouper_custom_args
        
        
        active_distinguisher.destination_name = self.groupdists
        
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

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        context.window_manager.invoke_props_dialog(self, width=230)
        return {"RUNNING_MODAL"}

op_class = GROUPER_OT_MDistAdd
