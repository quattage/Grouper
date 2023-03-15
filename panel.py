import bpy
from bpy.props import EnumProperty
from bpy.types import Panel, PropertyGroup
from .utils.logger import logger
from . import meshdist

high_items = [meshdist.MD_Midpoint(), meshdist.MD_UVSets()]
low_items = [meshdist.MD_Midpoint()]


class GROUPER_PT_EnumProperties(PropertyGroup):
    high_distinguishers: EnumProperty(items="", name='Highpoly Distinguishers')
    low_distinguishers: EnumProperty(items="", name='Highpoly Distinguishers')


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
        layout = self.layout
        box = layout.box()
        box.label(text="" + props.high_collection_name)
        row = box.row(heading="pee")
        row.operator('grouper.dist_add', icon="ADD", text="")
        row.operator('grouper.dist_remove', icon="REMOVE", text="")
        for entry in high_items:
            row = box.row()
            row.label(text="" + entry.name)
        box = layout.box()
        box.label(text="" + props.low_collection_name)
        for entry in low_items:
            row = box.row()
            row.label(text="" + entry.name)
        
        props.low_collection_name

def draw_distinguishers(layout, context):
    distlist = meshdist.get_distinguishers()
    logger.log(distlist)
    for dist in distlist:
        col = layout.row()
        thisdist = distlist[dist]
        col.label(text=thisdist.identifier + ": " + thisdist.name)
        

