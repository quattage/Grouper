import bpy
from bpy.props import BoolProperty, EnumProperty, IntProperty, StringProperty
from bpy.types import PropertyGroup
from bpy.types import AddonPreferences
from .distinguishers import groupdist


def ui_refresh(self, context):
    for region in context.area.regions:
        if region.type == "UI":
            region.tag_redraw()
    return None


class GROUPER_PT_PrefsProperties(PropertyGroup):
    low_suffix: StringProperty(description="Suffix to append to lowpoly objects.", default="_low")
    high_suffix: StringProperty(description="Suffix to append to highpoly objects", default="_high")
    low_collection_name: StringProperty(description="Name of the collections that store lowpoly objects", default="Lowpoly")
    high_collection_name: StringProperty(description="Name of the collections that store highpoly objects", default="Highpoly")

    bpy.types.Scene.grouper_mdlist_index = IntProperty(name="MDList Index", default=0, update=ui_refresh)
    bpy.types.Scene.grouper_gdlist_index = IntProperty(name="GDList Index", default=0, update=ui_refresh)


class GROUPER_PT_MDList(PropertyGroup):
    name: StringProperty(default="")
    identifier: StringProperty(default="")
    icon_name: StringProperty(default="")
    custom_args: StringProperty(default="")
    condition: BoolProperty()
    destination_name: StringProperty(default="")
    description: StringProperty(default="")


class GROUPER_PT_GDList(PropertyGroup):
    group_name: StringProperty(default="")
    identifier: StringProperty(default="")
    suffix_name: StringProperty(default="")
    icon_name: StringProperty(default="")


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