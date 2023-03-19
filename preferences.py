import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty
from bpy.types import PropertyGroup
from bpy.types import AddonPreferences


class GROUPER_PT_PrefsProperties(PropertyGroup):
    low_suffix: StringProperty(description="Suffix to append to lowpoly objects.", default="_low")
    high_suffix: StringProperty(description="Suffix to append to highpoly objects", default="_high")
    low_collection_name: StringProperty(description="Name of the collections that store lowpoly objects", default="Lowpoly")
    high_collection_name: StringProperty(description="Name of the collections that store highpoly objects", default="Highpoly")

class GROUPER_PT_MDList(PropertyGroup):
    name: StringProperty(default="")
    identifier: StringProperty(default="")
    icon_name: StringProperty(default="")
    custom_args: StringProperty(default="")
    condition: BoolProperty(default=True)
    destination_name: StringProperty(default="")
    description: StringProperty(default="")
    

class GROUPER_PT_GDList(PropertyGroup):
    name: StringProperty(default="")
    identifier: StringProperty(default="")

class GROUPER_PT_PrefsPanel(AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        props = bpy.context.scene.GROUPER_PT_PrefsProperties
        layout = self.layout
        box = layout.box()
        box.label(text="Convention Settings")
        row = box.row(align=True)
        row.label(text="Suffixes:")
        row.prop(props, "low_suffix", text="Low")
        row.prop(props, "high_suffix", text="High")

        row = box.row(align=True)
        row.label(text="Collections:")
        row.prop(props, "low_collection_name", text="Low")
        row.prop(props, "high_collection_name", text="High")

        box = layout.box()
        box.label(text="Misc Settings")
        row = box.row(align=True)
        row.label(text="!! work in progress !!")