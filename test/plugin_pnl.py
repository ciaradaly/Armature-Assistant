import bpy

from bpy.types import Panel
from bpy.props import *

from . plugin_op import ButtonOperator

class OBJECT_PT_MyPanel(Panel):
    bl_idname = "object.my_panel"
    bl_label = "Armature Assistant"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Plugin"
    bl_context = "objectmode"
    @classmethod
    def poll(self,context):
        return context.object is not None

    bpy.types.Scene.MyInt = IntProperty(name="MyInt", description="MyInt", min=0, max=255, default=0)

    def draw(self, context):
        
        layout = self.layout # .operator("scene.button_operator")
        #layout.prop(context.scene, "MyInt", slider=True)
        
        layout.operator('object.button_operator', text="Add new Bezier Curve", icon="CURVE_BEZCURVE").action='BEZIER_SPAWN'
        layout.operator('object.button_operator', text="Move to Center", icon="GRID").action='LOCATION'
        layout.operator('object.button_operator', text="Top", icon="CONSOLE").action='VIEW_TOP'
        layout.operator('object.button_operator', text="Side", icon="CONSOLE").action='VIEW_SIDE'
        layout.operator('object.button_operator', text="Front", icon="CONSOLE").action='VIEW_FRONT'
        layout.operator('object.button_operator', text="Bone converter", icon="CONSOLE").action='CONVERT_BONES'
        layout.prop(context.scene, 'MyInt', slider=True)
        layout.operator('object.button_operator', text="Change Frequency", icon="CONSOLE").action='BONE_FREQ'
        
        # row = layout.row()
        # col = row.column(align=True)
        # layout.label(text="Location adjustment:")
        # # col.label(text = str(obj.location))
        # col = layout.column(align=True)
        # col.operator(ButtonOperator.bl_idname, text="Change Location", icon="CONSOLE")
        
        # col.operator(ChangeViewpointOperator.bl_idname, text="Change ViewPoint", icon="CONSOLE")
