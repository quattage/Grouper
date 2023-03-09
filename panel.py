import bpy


class GROUPER_PT_OpsPanel(bpy.types.Panel):
    bl_label = "Grouper Conventions"
    bl_idname = "GROUPER_PT_OpsPanel"
    bl_category = "Grouper"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.operator('grouper.gen_collections', text='Generate Collections')
        box = layout.box()
        box.operator('grouper.test', text='Test')
        box = layout.box()
        col = box.column()
        col.label(text="Temporary Header")
        row = col.row()
        
        row = col.row()

        box = layout.box()
        col = box.column()
        col.label(text="Distinction")
        
        col = box.column()
        row = col.row()
        row.prop(context.scene, "use_modifiers")
        
        row = col.row()
        row.enabled = not context.scene.use_modifiers
        row.prop(context.scene, "poly_midpoint")
        row.operator('grouper.calc_midpoint', text='Calculate')



