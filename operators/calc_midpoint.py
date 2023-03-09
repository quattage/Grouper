import bpy
from ..utils.logger import logger


class GROUPER_OT_CalcMidpoint(bpy.types.Operator):
    bl_idname = "grouper.calc_midpoint"
    bl_label = "Calculate"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_description = 'Automatically sets the Midpoint value to the average polycount of the selection'

    def execute(self, context):
        selection = bpy.context.selected_objects
        polycounts = []
        if len(selection) > 1:
            if any(not obj.type == "MESH" for obj in selection):
                self.report({'ERROR'}, "Calculate midpoint: Selected objects must all be meshes!")
                return {'CANCELLED'}
            for obj in selection:
                depsgraph = bpy.context.evaluated_depsgraph_get()
                obj_evaluated = obj.evaluated_get(depsgraph)
                polycounts.append(len(obj_evaluated.data.polygons))
        else:
            self.report({'ERROR'}, "Calculate midpoint: Must have at least two selected objects!")
            return {'CANCELLED'}
        logger.log("Calculating Midpoint", "")

        polycounts.sort()
        middle = len(polycounts) // 2
        median = int((polycounts[middle] + polycounts[~middle]) // 2)

        bpy.context.scene.poly_midpoint = median
        self.report({'INFO'}, "Calculated a midpoint of " + str(median) + " polygons from " + str(len(selection)) + " mesh objects.")

        return {'FINISHED'}


op_class = GROUPER_OT_CalcMidpoint
