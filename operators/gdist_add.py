import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import Operator
from ..utils.general import stringutils
from ..distinguishers import groupdist



def colors(self, context) -> list:
    names = [
        ("OUTLINER_COLLECTION", "0", "Accessable as (OUTLINER_COLLECTION) in interface/themes", "OUTLINER_COLLECTION", 0),
        ("COLLECTION_COLOR_01", "1", "Accessable as (COLLECTION_COLOR_01) in interface/themes", "COLLECTION_COLOR_01", 1),
        ("COLLECTION_COLOR_01", "2", "Accessable as (COLLECTION_COLOR_01) in interface/themes", "COLLECTION_COLOR_01", 2),
        ("COLLECTION_COLOR_03", "3", "Accessable as (COLLECTION_COLOR_03) in interface/themes", "COLLECTION_COLOR_03", 3),
        ("COLLECTION_COLOR_04", "4", "Accessable as (COLLECTION_COLOR_04) in interface/themes", "COLLECTION_COLOR_04", 4),
        ("COLLECTION_COLOR_05", "5", "Accessable as (COLLECTION_COLOR_05) in interface/themes", "COLLECTION_COLOR_05", 5),
        ("COLLECTION_COLOR_06", "6", "Accessable as (COLLECTION_COLOR_06) in interface/themes", "COLLECTION_COLOR_06", 6),
        ("COLLECTION_COLOR_07", "7", "Accessable as (COLLECTION_COLOR_07) in interface/themes", "COLLECTION_COLOR_07", 7),
        ("COLLECTION_COLOR_08", "8", "Accessable as (COLLECTION_COLOR_08) in interface/themes", "COLLECTION_COLOR_08", 8)
    ]
    return names


class GROUPER_OT_GDistAdd(Operator):
    bl_idname = 'grouper.gdist_add'
    bl_label = 'Add Group'
    bl_description = 'Add a Collection to the list of Group Distinguishers'
    bl_options = {"UNDO"}

    name: StringProperty(default="", name = "", description="Collection Name")
    suffix: StringProperty(default="", name = "", description="Object suffix name")
    colors: EnumProperty(items=colors, name="", description="Collection color in the Outliner")

    def execute(self, context):
        gdlist = bpy.context.scene.grouper_gdlist
        
        if not self.name:
            self.report({"ERROR"}, "Collection name must not be blank!")
            return {'CANCELLED'}
        
        if not self.suffix:
            self.report({"INFO"}, "Collection '" + self.name + "' was initialized with a blank suffix")
        
        existing_names = []
        for obj in gdlist:
            existing_names.append(obj.group_name.upper())
        
        compare = self.name.upper()
        if compare in existing_names:
            self.report({"ERROR"}, "Name '" + self.name + "' already taken!")
            return {'CANCELLED'}
        
        groupdist.register_group(self.name, stringutils.formatsuffix(self.suffix), self.colors, context)
        context.scene.grouper_gdlist_index = len(context.scene.grouper_gdlist) - 1
        
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
        return context.window_manager.invoke_props_dialog(self, width=200)


op_class = GROUPER_OT_GDistAdd
