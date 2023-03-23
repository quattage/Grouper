import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import Operator
from ..utils.general import stringutils
from ..distinguishers import groupdist



def colors(self, context) -> list:
    names = [
        ("OUTLINER_COLLECTION", "0", "Accessable as (OUTLINER_COLLECTION) in interface/themes", "OUTLINER_COLLECTION", 0),
        ("COLLECTION_COLOR_01", "1", "Accessable as (COLLECTION_COLOR_01) in interface/themes", "COLLECTION_COLOR_01", 1),
        ("COLLECTION_COLOR_02", "2", "Accessable as (COLLECTION_COLOR_02) in interface/themes", "COLLECTION_COLOR_02", 2),
        ("COLLECTION_COLOR_03", "3", "Accessable as (COLLECTION_COLOR_03) in interface/themes", "COLLECTION_COLOR_03", 3),
        ("COLLECTION_COLOR_04", "4", "Accessable as (COLLECTION_COLOR_04) in interface/themes", "COLLECTION_COLOR_04", 4),
        ("COLLECTION_COLOR_05", "5", "Accessable as (COLLECTION_COLOR_05) in interface/themes", "COLLECTION_COLOR_05", 5),
        ("COLLECTION_COLOR_06", "6", "Accessable as (COLLECTION_COLOR_06) in interface/themes", "COLLECTION_COLOR_06", 6),
        ("COLLECTION_COLOR_07", "7", "Accessable as (COLLECTION_COLOR_07) in interface/themes", "COLLECTION_COLOR_07", 7),
        ("COLLECTION_COLOR_08", "8", "Accessable as (COLLECTION_COLOR_08) in interface/themes", "COLLECTION_COLOR_08", 8)
    ]
    return names


class GROUPER_OT_GDistEdit(Operator):
    bl_idname = 'grouper.gdist_edit'
    bl_label = 'Edit Group'
    bl_description = 'Edit an existing Group Collection'
    bl_options = {"UNDO"}

    name: StringProperty(default="", name = "", description="Collection Name")
    suffix: StringProperty(default="", name = "", description="Object suffix name")
    colors: EnumProperty(items=colors, name="", description="Collection color in the Outliner")

    def execute(self, context):
        gdlist = bpy.context.scene.grouper_gdlist
        gdlist_index = bpy.context.scene.grouper_gdlist_index
        
        if not self.name:
            self.report({"ERROR"}, "Collection name must not be blank!")
            return {'CANCELLED'}
        
        if not self.suffix:
            self.report({"INFO"}, "Collection '" + self.name + "' was reinitialized with a blank suffix")
        
        gdlist.remove(gdlist_index)
        
        groupdist.register_group(self.name, stringutils.formatsuffix(self.suffix), self.colors, context)
        gdlist.move(len(context.scene.grouper_gdlist) - 1, gdlist_index)
        context.scene.grouper_gdlist_index = gdlist_index         # this is literally just to force a refresh callback on the uilist, i am sorry this is dumb
        
        return {'FINISHED'}
    

    def draw(self, context):
        layout = self.layout
        options = layout.box().column()
        
        namesel = options.row()
        namesel.label(text="Name:")
        namesel.label(icon="DISCLOSURE_TRI_RIGHT")
        namesel.prop(self, "name")
        
        suffixsel = options.row()
        suffixsel.label(text="Suffix:")
        suffixsel.label(icon="DISCLOSURE_TRI_RIGHT")
        suffixsel.prop(self, "suffix")
        
        colorsel = options.row()
        colorsel.label(text="Color:")
        colorsel.label(icon="DISCLOSURE_TRI_RIGHT")
        colorsel.prop(self, "colors")
        
        display = layout.box().row()
        if self.name:
            display.label(icon=self.colors, text=self.name)
        else:
            display.label(icon="ERROR", text="No name")
        if self.suffix:
            display.label(icon="DISCLOSURE_TRI_RIGHT", text=stringutils.formatsuffix(self.suffix))
        else:
            display.label(icon="DISCLOSURE_TRI_RIGHT", text="No suffix")
        
        
    def invoke(self, context, event):
        gdlist = context.scene.grouper_gdlist
        gdlist_index = context.scene.grouper_gdlist_index
        active = gdlist[gdlist_index]
        if active:
            self.name = active.group_name
            self.suffix = active.suffix_name
            self.colors = active.icon_name
        
        return context.window_manager.invoke_props_dialog(self, width=200)


op_class = GROUPER_OT_GDistEdit
