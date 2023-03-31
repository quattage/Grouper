import bpy
from ..utils.logger import logger

class GROUPER_OT_ExportGroups(bpy.types.Operator):
    bl_idname = "grouper.export_groups"
    bl_label = "Export Groups"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_description = 'Automatically exports groups with their own settings.'

    def execute(self, context):
        return {'FINISHED'}

    def draw(self, context):
        exports = bpy.context.scene.grouper_for_export
        groups = bpy.context.scene.grouper_gdlist
        layout = self.layout
        
        layout.prop(bpy.context.scene.grouper_prefs, "export_path", text="")
        
        vgcont = layout.column(align=True)
        for groupflag in exports:
            item = vgcont.box().row()
            group = groups[groupflag.index]
            itemname = item.row()
            itemname.label(icon=group.icon_name, text=group.group_name)
            itemname.enabled = groupflag.do_export
            item.prop(groupflag, "do_export", text="")

    def invoke(self, context, event):
        bpy.context.scene.grouper_for_export.clear()
        exports = bpy.context.scene.grouper_for_export
        gdlist = context.scene.grouper_gdlist
        for ind, obj in enumerate(gdlist):
            if obj.export_settings:
                newexport = exports.add()
                newexport.index = ind
                newexport.do_export = True
                logger.log("Marked group for export: " + obj.group_name + " at index " + str(ind), "DEBUG")
                
        return context.window_manager.invoke_props_dialog(self, width=250)


op_class = GROUPER_OT_ExportGroups
