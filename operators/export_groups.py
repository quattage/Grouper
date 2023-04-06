import bpy
from bpy.props import BoolProperty
from ..utils.logger import logger
from ..utils import collman, objman

class GROUPER_OT_ExportGroups(bpy.types.Operator):
    bl_idname = "grouper.export_groups"
    bl_label = "Export Groups"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_description = 'Automatically exports groups with their own settings.'

    combine: BoolProperty(default=False)

    def execute(self, context):
        all_exports = list(bpy.context.scene.grouper_for_export)
        all_exports[:] = [obj for obj in all_exports if obj.do_export]
        groups = bpy.context.scene.grouper_gdlist
        path_members = bpy.context.scene.grouper_prefs.export_path.split("\\")
        export_name = path_members[len(path_members) - 1]
        export_dir = ""

        if export_name:
            export_dir = bpy.context.scene.grouper_prefs.export_path.rsplit("\\", 1)[0] + "\\"
        else:
            export_dir = bpy.context.scene.grouper_prefs.export_path
            export_name = "none"

        if self.combine:
            pass # later.
        else:
            if not all_exports:
                self.report({"ERROR"}, "Must have at least one group selected for export!")
                return {"CANCELLED"}
            for obj in all_exports:
                group = groups[obj.index]
                filename = export_name + group.suffix_name
                logger.log("Exporting '" + filename + "' to " + export_dir)
                
                # check if the collections exist
                active_collection = collman.is_created(group.group_name)
                if (not active_collection) or (not collman.is_linked(active_collection)):
                    self.report({"ERROR"}, "Collection '" + group.group_name + "' does not exist in the outliner!")
                    return {"CANCELLED"}
                
                # check if the collections contain meshes
                collection_children = objman.get_children(active_collection)
                collection_children[:] = [obj for obj in collection_children if obj.type == "MESH"]
                if not collection_children:
                    self.report({"ERROR"}, "Collection '" + group.group_name + "' contains no mesh objects!")
                    return {"CANCELLED"}
                
                # loop through mesh objects and select them
                for obj in collection_children:
                    obj.select_set(True)
                
                
    
        return {'FINISHED'}
    

    def draw(self, context):
        exports = bpy.context.scene.grouper_for_export
        groups = bpy.context.scene.grouper_gdlist
        layout = self.layout
        
        cont = layout.column(align=True)
        
        exports = bpy.context.scene.grouper_for_export
        groups = bpy.context.scene.grouper_gdlist
        pathrow = cont.row()
        
        path_members = bpy.context.scene.grouper_prefs.export_path.split("\\")
        export_name = path_members[len(path_members) - 1]
        export_name = "none" if not export_name else export_name
        
        if not self.combine:
            for groupflag in exports:
                item = cont.box().row()
                group = groups[groupflag.index]
                itemname = item.row()
                itemname.label(icon="MESH_CUBE")
                itemname.label(icon=group.icon_name, text=export_name + group.suffix_name)
                itemname.enabled = groupflag.do_export
                item.prop(groupflag, "do_export", text="")
        else:
            item = cont.box().row()
            item.label(icon="MESH_CUBE")
            item.label(icon="OUTLINER_COLLECTION", text=export_name + "_all")
            
        cont.separator()
        
        comb = cont.row(align=True)
        comb.prop(self, "combine", toggle=True, text="Combined")
        comb.prop(self, "combine", toggle=True, invert_checkbox=True, text="Individual")
        
        if self.combine:
            cont.separator()
            props = cont.box().column(align=True)


    def invoke(self, context, event):
        bpy.context.scene.grouper_for_export.clear()
        exports = bpy.context.scene.grouper_for_export
        gdlist = context.scene.grouper_gdlist
        
        if not context.scene.grouper_prefs.export_path:
            self.report({"ERROR"}, "Export path not assigned.")
            return {"CANCELLED"}
    
        for ind, obj in enumerate(gdlist):
            if obj.export_settings:
                newexport = exports.add()
                newexport.index = ind
                newexport.do_export = True
                logger.log("Marked group for export: '" + obj.group_name + "' at index " + str(ind), "DEBUG")
                
        return context.window_manager.invoke_props_dialog(self, width=200)

op_class = GROUPER_OT_ExportGroups
