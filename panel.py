import bpy
from bpy.props import EnumProperty
from bpy.types import Panel, PropertyGroup
from .utils.logger import logger
from . import meshdist

mid = meshdist.MD_Midpoint()

high_items = [
    (mid.identifier, mid, "")
]

low_items = [
    (mid.identifier, mid, "")
]

def populate_enums(distlist):
    enum_items = []
    for i, entry in enumerate(distlist):
        enum_items.append((entry[0], entry[0], str(entry[1]), i))
        print("piss manufacturing: " + str(enum_items))
    return enum_items


def add_item(dist, lst):
    lst.append(dist)
    populate_enums(lst)


class GROUPER_PT_EnumProperties(PropertyGroup):
    high_distinguishers: EnumProperty(items=populate_enums(high_items), name='Highpoly Distinguishers')
    low_distinguishers: EnumProperty(items=populate_enums(low_items), name='Lowpoly Distinguishers')


class GROUPER_PT_OpsPanel(Panel):
    bl_label = "Grouper Conventions"
    bl_idname = "GROUPER_PT_OpsPanel"
    bl_category = "Grouper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('grouper.gen_collections', text='Generate')
        row.operator('grouper.test', text='Test')
        row = layout.row()
        row.operator('grouper.test', text='Sort')
        row = layout.row()
        draw_distinguishers(layout, context)
        row = layout.row()
        row.prop(context.scene, "poly_midpoint")
        row.operator('grouper.calc_midpoint', text='Calculate')


class GROUPER_PT_EnumsPanel(Panel):
    bl_label = "Distinguishers"
    bl_idname = "GROUPER_PT_EnumsPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "GROUPER_PT_OpsPanel"

    def draw(self, context):
        props = props = bpy.context.scene.GROUPER_PT_PrefsProperties
        global enums
        enums = bpy.context.scene.GROUPER_PT_EnumProperties

        layout = self.layout
        box = layout.box()
        box.label(text="" + props.high_collection_name)
        row = box.row()
        row.operator('grouper.dist_add', icon="ADD", text="")

        logger.log("the high piss: " + enums.high_distinguishers + "   ...end of high piss!")
        logger.log("the low piss: " + enums.low_distinguishers + "   ...end of low piss!")

        for entry in enums.high_distinguishers:
            row = box.row()
            row.label(text="" + entry.name)
            op = row.operator('grouper.dist_remove', icon="REMOVE", text="")
            op.use_low = False
            op.obj_to_remove = entry.name
        box = layout.box()
        box.label(text="" + props.low_collection_name)

        for entry in enums.low_distinguishers:
            row = box.row()
            row.label(text="" + entry.name)
            op = row.operator('grouper.dist_remove', icon="REMOVE", text="")
            op.use_low = True
            op.obj_to_remove = entry.name

        props.low_collection_name


def set_defaults():
    mid = meshdist.MD_Midpoint()
    add_item(mid, high_items)

    mid = meshdist.MD_Midpoint()
    add_item(mid, low_items)


def draw_distinguishers(layout, context):
    distlist = meshdist.get_distinguishers()
    for dist in distlist:
        col = layout.row()
        thisdist = distlist[dist]
        col.label(text=thisdist.identifier + ": " + thisdist.name)



