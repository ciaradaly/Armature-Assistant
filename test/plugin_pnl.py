import bpy

from bpy.types import Panel

class CD_PT_PANEL(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Modifier operations"
    bl_category = "Display Info"

    def draw(self, context):

        layout = self.layout

        layout = self.layout

        box = layout.box()

        for obj in bpy.data.objects:
            print(obj.name)
            # 2 columns with button
            row = layout.row()
            col = row.column()
            col.label(text = obj.name)
