import bpy
from bpy.types import Panel, UIList
from .preferences import GROUPER_PT_MDList
from .distinguishers import meshdist
from .utils.general import stringutils, listutils


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
        scene = context.scene
        layout = self.layout

        mdlist = bpy.context.scene.grouper_mdlist
        mdlist_index = bpy.context.scene.grouper_mdlist_index

        draw_mdlist_viewer(scene, layout, mdlist, mdlist_index)
        layout.separator()

        gdlist = bpy.context.scene.grouper_gdlist
        gdlist_index = bpy.context.scene.grouper_gdlist_index
        draw_gdlist_select(scene, layout, gdlist, gdlist_index)
        

def draw_mdlist_viewer(scene, layout, mdlist, mdlist_index):
    layout.label(icon="FILE_VOLUME", text="Mesh Distinguishers")
    row = layout.row(align=True)
    adjustmentscoll = row.column(align=True)
    adjustmentbox = adjustmentscoll.box()
    listcoll = row.column(align=True)
    listcoll.template_list("GROUPER_UL_MDViewer", "MD_List", scene, "grouper_mdlist", scene, "grouper_mdlist_index")
    add_button = adjustmentbox.column(align=True)
    add_button.operator('grouper.dist_add', icon="ADD", text="")

    active_item = listutils.get_active(mdlist, mdlist_index)
    sub_button = add_button.row(align=True)
    sub_button.operator('grouper.dist_remove', icon="REMOVE", text="")
    sub_button.enabled = listutils.is_positional(mdlist) and isinstance(active_item, GROUPER_PT_MDList)

    move_buttons = add_button.column(align=True)
    move_buttons.enabled = listutils.get_active(mdlist, mdlist_index) and listutils.is_positional(mdlist)

    move_buttons_up = move_buttons.row(align=True)
    move_buttons_up.operator('grouper.dist_up', icon="TRIA_UP", text="")
    move_buttons_up.enabled = listutils.can_move_up(mdlist_index)

    move_buttons_down = move_buttons.row(align=True)
    move_buttons_down.operator('grouper.dist_down', icon="TRIA_DOWN", text="")
    move_buttons_down.enabled = listutils.can_move_down(mdlist, mdlist_index)
        
    helpbox = adjustmentscoll.box()
    helpbox.operator('grouper.dist_help', icon="QUESTION", text="")


def draw_gdlist_select(scene, layout, gdlist, gdlist_index):
    layout.label(icon="OUTLINER_COLLECTION", text="Group Distinguishers")
    row = layout.row(align=True)
    adjustmentscoll = row.column(align=True)
    adjustmentbox = adjustmentscoll.box()
    listcoll = row.column(align=True)
    listcoll.template_list("GROUPER_UL_GDViewer", "GD_List", scene, "grouper_gdlist", scene, "grouper_gdlist_index")
    add_button = adjustmentbox.column(align=True)
    add_button.operator('grouper.gdist_add', icon="ADD", text="")

    sub_button = add_button.row(align=True)
    sub_button.operator('grouper.gdist_remove', icon="REMOVE", text="")
    sub_button.enabled = listutils.is_positional(gdlist)

    move_buttons = add_button.column(align=True)
    move_buttons.enabled = listutils.get_active(gdlist, gdlist_index) and listutils.is_positional(gdlist)

    move_buttons_up = move_buttons.row(align=True)
    move_buttons_up.operator('grouper.gdist_up', icon="TRIA_UP", text="")
    move_buttons_up.enabled = listutils.can_move_up(gdlist_index)

    move_buttons_down = move_buttons.row(align=True)
    move_buttons_down.operator('grouper.gdist_down', icon="TRIA_DOWN", text="")
    move_buttons_down.enabled = listutils.can_move_down(gdlist, gdlist_index)
        
    helpbox = adjustmentscoll.box()
    helpbox.operator('grouper.gdist_help', icon="QUESTION", text="")


class GROUPER_UL_GDViewer(UIList):
    def draw_filter(self, context, layout):
        gdlist = bpy.context.scene.grouper_gdlist
        gdlist_index = bpy.context.scene.grouper_gdlist_index
        
        inspector = layout.box()
        info = inspector.row(align=True).box()
        active_item = listutils.get_active(gdlist, gdlist_index)
        
        
        if not active_item:
            info.label(icon="FILE_BLANK", text="No group selected.")
            helpdesc = inspector.column()
            helpdesc.label(text="What is this?", icon="OUTLINER_OB_LIGHT")
            helpcont = helpdesc.box()
            stringutils.wrap("This panel contains a list of collections. These are where objects will end up when they get sorted.", helpcont)
            stringutils.wrap("The list order doesn't matter, but it will be retained in the Outliner. You can push changes to the Outliner by pressing the 'Generate' button.", helpcont)
        else:
            la = info.row()
            la.label(text=active_item.group_name)
            
            la.operator('grouper.gdist_edit', icon="MODIFIER_ON", text="")
            
        
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj = item
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.label(text=obj.group_name, icon=obj.icon_name)
            if obj.suffix_name:
                row.label(text=obj.suffix_name, icon="DISCLOSURE_TRI_RIGHT")
            else:
                nosuf = row.row()
                nosuf.label(text="No Suffix", icon="LAYER_USED") 
                nosuf.enabled = False
                


class GROUPER_UL_MDViewer(UIList):
    def draw_filter(self, context, layout):
        mdlist = bpy.context.scene.grouper_mdlist
        mdlist_index = bpy.context.scene.grouper_mdlist_index
        
        inspector = layout.box()
        icontent_header = inspector.row(align=True)
        active_item = listutils.get_active(mdlist, mdlist_index)
        
        
        """
        .name -> str
        .identifier -> str
        .icon_name -> str
        .custom_args -> dict AS STR
        .condition -> bool
        .destination_name -> str
        """

        if not active_item:
            icontent_header.label(icon="FILE_BLANK")
            stringutils.wrap("Select a distinguisher to get started.", icontent_header, 28)
            helpdesc = inspector.column()
            helpdesc.label(text="What is this?", icon="OUTLINER_OB_LIGHT")
            helpcont = helpdesc.box()
            stringutils.wrap("In this panel you'll find a list of objects, called 'Distinguishers.'\nThese Distinguishers let you specify what mesh characteristics Grouper considers when it sorts meshes.", helpcont)
            stringutils.wrap("The list above is sorted by priority, where the highest entry is considered first.", helpcont)
        else:
            item = meshdist.serialize(active_item)
            icontent_header.label(icon="FILE_VOLUME")
            icontent_header.label(text=" " + item.name)
            icontent_header.operator('grouper.dist_add', icon="MODIFIER_ON", text="")

            infoview = inspector.column(align=True)
            infoview.label(icon="HELP", text="Description:")
            if item.description:
                stringutils.wrap(item.description + ", move the object to '" + item.destination_name + "'", infoview.box())
            else:
                stringutils.wrap("'" + item.name + "' has no description. You may wanna report this.", infoview.box())
                
            cond= infoview.box().row(align=True)
            cond.label(icon="KEYFRAME", text="Condition")
            cond.label(icon="DISCLOSURE_TRI_RIGHT", text=stringutils.formatvalue(item.condition))
            gdlist = context.scene.grouper_gdlist
            
            if not listutils.get_gd_from_name(gdlist, item.destination_name):
                infoview.separator()
                infoview.label(icon="ERROR", text= "WARNING!")
                warning = infoview.box()
                stringutils.wrap("A collection called '" + item.destination_name + "'" + " does not exist. Sorting will not work!", warning)

            argsview = inspector.column(align=True)
            argsview.separator()
            argsview_header= argsview.row(align=True)
            argsview_header.label(icon="FILE_CACHE",text="Custom Arguments:")
            for key, value in item.custom_args.items():
                arg = argsview.box().row(align=True)
                arg.label(icon="KEYFRAME", text=stringutils.formatkey(key))
                arg.label(icon="DISCLOSURE_TRI_RIGHT", text=stringutils.formatvalue(value))

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        obj = item
        custom_icon = obj.icon_name
        gdlist = context.scene.grouper_gdlist

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.label(text="", icon=custom_icon)
            row.label(text=" " + obj.name)
            row.label(icon="FORWARD")
            
            gdobj = listutils.get_gd_from_name(gdlist, item.destination_name) 
            if not gdobj:
                row.label(icon="SEQUENCE_COLOR_01", text="INVALID")
            else:
                row.label(icon=gdobj.icon_name, text=obj.destination_name)

        elif self.layout_typoe in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="", icon=custom_icon)
            
            


