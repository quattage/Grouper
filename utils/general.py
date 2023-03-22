
import textwrap
import bpy

from bpy.types import EnumProperty

class listutils:
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
    
    
    def get_gd_from_name(dlist, name):
        for obj in dlist:
            if obj.group_name == name:
                return obj
        return None

class stringutils:
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