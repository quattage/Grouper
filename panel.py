import bpy
from bpy.props import BoolProperty
from bpy.types import Panel, UIList
from .utils.logger import logger


def populate_enums(distlist):
    enum_items = []
    for i, entry in enumerate(distlist):
        enum_items.append((entry[0], entry[0], str(entry[1]), i))
    print(enum_items)
    
    return enum_items


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
        prefs = bpy.context.scene.grouper_prefs      
        scene = context.scene
        
        layout = self.layout
        layout.label(text="" + "Mesh")
        row = layout.row()
        row.template_list("GROUPER_UL_MDViewer", "MD_List", scene, "grouper_mdlist", scene, "grouper_mdlist_index")
        box = layout.box()
        row = box.row(align=True)
        row.operator('grouper.dist_add', icon="ADD", text="")
        row.operator('grouper.dist_remove', icon="REMOVE", text="")
        
        


class GROUPER_UL_MDViewer(UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propnale, index):
        scene = data
        obj = item
        
        custom_icon = obj.icon_name
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            print("distobj: " + obj.name + ", " + obj.identifier + ", " + obj.icon_name + ", " + obj.custom_args + ", " + str(obj.condition) + ", " + obj.destination_name)
            row = layout.row()
            row.label(text="", icon = custom_icon)
            row.label(text=obj.name)
            row.label(icon="FORWARD")
            minus = row.operator('grouper.dist_remove', text="", icon="REMOVE")
            minus.to_remove = obj.name
        
        elif self.layout_typoe in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="", icon=custom_icon)
            