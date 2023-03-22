import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import Operator, Panel
from ..utils.logger import logger
from ..distinguishers import meshdist, groupdist


def colors(self, context) -> list:
    names = [
        ("COL_00", "0", "Accessable as (OUTLINER_COLLECTION) in interface/themes", "OUTLINER_COLLECTION", 0),
        ("COL_01", "1", "Accessable as (COLLECTION_COLOR_01) in interface/themes", "COLLECTION_COLOR_01", 1),
        ("COL_02", "2", "Accessable as (COLLECTION_COLOR_01) in interface/themes", "COLLECTION_COLOR_01", 2),
        ("COL_03", "3", "Accessable as (COLLECTION_COLOR_03) in interface/themes", "COLLECTION_COLOR_03", 3),
        ("COL_04", "4", "Accessable as (COLLECTION_COLOR_04) in interface/themes", "COLLECTION_COLOR_04", 4),
        ("COL_05", "5", "Accessable as (COLLECTION_COLOR_05) in interface/themes", "COLLECTION_COLOR_05", 5),
        ("COL_06", "6", "Accessable as (COLLECTION_COLOR_06) in interface/themes", "COLLECTION_COLOR_06", 6),
        ("COL_07", "7", "Accessable as (COLLECTION_COLOR_07) in interface/themes", "COLLECTION_COLOR_07", 7),
        ("COL_08", "8", "Accessable as (COLLECTION_COLOR_08) in interface/themes", "COLLECTION_COLOR_08", 8)
    ]
    return names


class GROUPER_OT_GDistAdd(Operator):
    bl_idname = 'grouper.gdist_add'
    bl_label = 'Add Collection Group'
    bl_description = 'Add a Collection Group to the list'

    name: StringProperty(default="", name = "", description="Collection Name")
    suffix: StringProperty(default="", name = "", description="Object suffix name")
    colors: EnumProperty(items=colors, name="", description="Collection color in the Outliner")

    def execute(self, context):
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
        display.label(icon=colors)
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=170)


op_class = GROUPER_OT_GDistAdd
