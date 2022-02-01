import bpy

from bpy.types import Operator
from bpy.props import EnumProperty

#Operates button functionalities on UI panel
class ButtonOperator(Operator):
    bl_idname = "object.button_operator"
    bl_label = "Button"
    action: EnumProperty(
        items=[
            ('LOCATION', 'change location', 'change location'),
            ('CHANGE_VIEW', 'change viewport', 'change viewport')
        ]
    )
    def execute(self, context):
        if self.action == 'LOCATION':
            self.change_location(context=context)
        if self.action == 'CHANGE_VIEW':
            self.change_viewport(context=context)
        return {'FINISHED'}

    @staticmethod
    def change_location(context):
        bpy.context.active_object.location = (0, 0, 0)
        return {'FINISHED'}

# class ChangeViewpointOperator(Operator):
#     bl_idname = "object.button_operator"
#     bl_label = "Test"
    @staticmethod
    def change_viewport(context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D': 
                ctx = {
                    "window": bpy.context.window, # Only change on window currently open
                    "area": area, # our 3D View (the first found only actually)
                    "region": None # just to suppress PyContext warning, doesn't seem to have any effect
                }
                bpy.ops.view3d.view_axis(type='LEFT', align_active=False)
                bpy.context.space_data.region_3d.update()
        return {'FINISHED'}
