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
    condition: BoolProperty(name="Condition", default=True)

    def execute(self, context):
        mdlist = context.scene.grouper_mdlist

        new_dist = meshdist.serialize_from_identifier(self.meshdist_types)
        new_dist.condition = self.condition
        new_dist.custom_args = meshdist.get_args_from_prop(context)
        new_dist.destination_name = self.groupdists

        dist_reference = mdlist.add()
        dist_reference.name = new_dist.name
        dist_reference.identifier = new_dist.identifier
        dist_reference.icon_name = new_dist.icon_name
        dist_reference.custom_args = json.dumps(new_dist.custom_args)
        dist_reference.condition = new_dist.condition
        dist_reference.destination_name = new_dist.destination_name

        dist_reference.description = new_dist.description
        context.scene.grouper_mdlist_index = len(context.scene.grouper_mdlist) - 1
        return {'FINISHED'}

    def draw(self, context):
        gdlist = bpy.context.scene.grouper_gdlist
        active_distinguisher = meshdist.serialize_from_identifier(self.meshdist_types)
        active_distinguisher.destination_name = self.groupdists
        args_instance = meshdist.get_args_from_prop(context)

        if args_instance:
            active_distinguisher.custom_args = args_instance
            logger.log("Applied custom arguments to Distinguisher instance: " + str(active_distinguisher.custom_args))

        active_distinguisher.set_description()
        logger.log(meshdist.get_args_from_prop(context))

        args = bpy.context.scene.grouper_custom_args
        layout = self.layout

        seldist = layout.row().split(factor=0.4)
        seldist.label(text="Type:")
        seldist.prop(self, "meshdist_types")

        selgroup = layout.row().split(factor=0.4)
        selgroup.label(text="Destination:")
        selgroup.prop(self, "groupdists", emboss=True)

        togglecond = layout.row().split(factor=0.4)
        togglecond.label(text="Condition:")
        if self.condition:
            togglecond.prop(self, "condition", toggle=True, text="Nominal (True)")
        else:
            togglecond.prop(self, "condition", toggle=True, text="Inverted (False)")

        argsettings = layout.column(align=True)
        argsettings.label(icon="FILE_CACHE",text="Custom Settings:")
        if len(args) > 0:
            for item in args:
                argument = argsettings.box().row()
                if item.arg_type == "bool":
                    argument.label(icon="KEYFRAME", text=stringutils.formatkey(item.arg_name))
                    if item.arg_bool:
                        argument.prop(icon="CHECKMARK", data=item, property="arg_bool", text="True", toggle=True)
                    else:
                        argument.prop(icon="X", data=item, property="arg_bool", text="False", toggle=True)
                elif item.arg_type == "str":
                    argument.label(icon="KEYFRAME", text=stringutils.formatkey(item.arg_name))
                    argument.prop(icon="KEYFRAME", data=item, property="arg_str", text="")
                elif item.arg_type == "int":
                    argument.label(icon="KEYFRAME", text=stringutils.formatkey(item.arg_name))
                    argument.prop(data=item, property="arg_int", text="")
        else:
            argument = argsettings.box().row()
            argument.label(icon="CANCEL", text="No additional settings")
            argument.enabled = False
            pass

        layout.separator()
        display = layout.column(align=True)
        display.label(icon="FILE_VOLUME", text="Distinguisher Output:")
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
            stringutils.wrap("Distinguisher '" + active_distinguisher.name + "' has no description (or no description was able to be made). You may wanna report this.", desc, 39)

    def invoke(self, context, event):
        context.scene.grouper_custom_args.clear()
        self.meshdist_types = "MD_Bevel"
        return context.window_manager.invoke_props_dialog(self, width=230)

op_class = GROUPER_OT_MDistAdd

