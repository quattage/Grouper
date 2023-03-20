import bpy, textwrap
from bpy.props import BoolProperty, IntProperty
from bpy.types import Panel, UIList
from .utils.logger import logger
from .distinguishers import meshdist


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
        mdlist = bpy.context.scene.grouper_mdlist
        mdlist_index = bpy.context.scene.grouper_mdlist_index
        scene = context.scene


        layout = self.layout
        layout.label(icon="FILE_VOLUME", text="Mesh Distinguishers")
        
        row = layout.row(align=True)
        adjustmentscoll = row.column(align=True)
        adjustmentbox = adjustmentscoll.box()
        listcoll = row.column(align=True)

        listcoll.template_list("GROUPER_UL_MDViewer", "MD_List", scene, "grouper_mdlist", scene, "grouper_mdlist_index")

        add_button = adjustmentbox.column(align=True)
        add_button.operator('grouper.dist_add', icon="ADD", text="")

        sub_button = add_button.row(align=True)
        sub_button.operator('grouper.dist_remove', icon="REMOVE", text="")
        sub_button.enabled = is_positional(mdlist)

        move_buttons = add_button.column(align=True)
        move_buttons.enabled = get_active(mdlist, mdlist_index) and is_positional(mdlist)

        move_buttons_up = move_buttons.row(align=True)
        move_buttons_up.operator('grouper.dist_add', icon="TRIA_UP", text="")
        move_buttons_up.enabled = can_move_up(mdlist_index)

        move_buttons_down = move_buttons.row(align=True)
        move_buttons_down.operator('grouper.dist_add', icon="TRIA_DOWN", text="")
        move_buttons_down.enabled = can_move_down(mdlist, mdlist_index)
        
        helpbox = adjustmentscoll.box()
        helpbox.operator('grouper.dist_help', icon="QUESTION", text="")


def get_active(mdlist, mdlist_index):
    try:
        active = mdlist[mdlist_index]
        return active
    except IndexError:
        return False


def is_positional(mdlist):
    if len(mdlist) > 1:
        return True
    return False


def can_move_up(mdlist_index) -> bool:
    return mdlist_index > 0


def can_move_down(mdlist, mdlist_index) -> bool:
    return mdlist_index < len(mdlist) - 1


class GROUPER_UL_MDViewer(UIList):
    def draw_filter(self, context, layout):
        prefs = bpy.context.scene.grouper_prefs 
        mdlist = bpy.context.scene.grouper_mdlist
        mdlist_index = bpy.context.scene.grouper_mdlist_index
        
        inspector = layout.box()
        icontent_header = inspector.row(align=True)
        active_item = get_active(mdlist, mdlist_index)
        
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
            wrap("Select a distinguisher to get started.", icontent_header, 28)
            helpdesc = inspector.column()
            helpdesc.label(text="What is this?", icon="OUTLINER_OB_LIGHT")
            helpcont = helpdesc.box()
            wrap("In this panel you'll find a list of objects, called 'Distinguishers.'\nThese Distinguishers let you specify what mesh characteristics Grouper considers when it sorts meshes.", helpcont)
            wrap("The list above is sorted by priority, where the highest entry is considered first.", helpcont)
        else:
            item = meshdist.serialize(active_item)
            icontent_header.label(icon="FILE_VOLUME")
            icontent_header.label(text=" " + item.name)

            infoview = inspector.column(align=True)
            infoview.label(icon="HELP", text="Description:")
            wrap(item.description + ", move the object to '" + item.destination_name + "'", infoview.box())

            argsview = inspector.column(align=True)
            argsview.separator()
            argsview_header= argsview.row(align=True)
            argsview_header.label(icon="FILE_CACHE",text="Custom Arguments:")
            argsview_header.operator('grouper.dist_add', icon="MODIFIER_ON", text = "")
            for key, value in item.custom_args.items():
                arg = argsview.box().row(align=True)
                arg.label(icon="KEYFRAME", text=formatkey(key))
                arg.label(icon="DISCLOSURE_TRI_RIGHT", text=formatvalue(value))
            
            arg = argsview.box().row(align=True)
            arg.label(icon="KEYFRAME", text="Condition")
            arg.label(icon="DISCLOSURE_TRI_RIGHT", text=formatvalue(item.condition))

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        scene = data
        obj = item
        custom_icon = obj.icon_name

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.label(text="", icon=custom_icon)
            row.label(text=" " + obj.name)
            row.label(icon="FORWARD")
            row.label(icon="OUTLINER_COLLECTION")
            row.label(text=obj.destination_name)

        elif self.layout_typoe in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text="", icon=custom_icon)


def formatvalue(value):
        out = ""
        if isinstance(value, str):
            out = "'" + value + "'"
        else:
            out = str(value)
        return out


def formatkey(key):
    return key.capitalize()


def wrap(text_to_wrap, element, w: int = 30):
    wrapper = textwrap.TextWrapper(width=w)
    textlist = wrapper.wrap(text=text_to_wrap)
    wrapped_block = element.column(align=True)
    for line in textlist:
        row = wrapped_block.row(align=True)
        row.scale_y = 0.6
        row.label(text=line)
    
    
    

    
    
