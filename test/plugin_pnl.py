import bpy

from bpy.types import Panel

from . plugin_op import ButtonOperator


class OBJECT_PT_MyPanel(Panel):
    bl_idname = "object.my_panel"
    bl_label = "Armature Assistant"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Plugin"
    bl_context = "objectmode"

    bpy.types.Scene.MyInt = bpy.props.IntProperty(name='MyInt', description="Amount of Bones", min=0, max=100, default=1)
    
    @classmethod
    def poll(self,context):
        return context.object is not None

    
    def draw(self, context):
        layout = self.layout # .operator("scene.button_operator")
        layout.operator('object.button_operator', text="Move to Center", icon="CONSOLE").action='LOCATION'
        layout.operator('object.button_operator', text="Change ViewPoint", icon="CONSOLE").action='CHANGE_VIEW'
        layout.operator('object.button_operator', text="Bone converter", icon="CONSOLE").action='CONVERT_BONES'

        layout.prop(bpy.context.scene, "MyInt", slider=True)
        # obj = bpy.context.selected_objects
        # row = layout.row()
        # col = row.column(align=True)
        # layout.label(text="Location adjustment:")
        # # col.label(text = str(obj.location))
        # col = layout.column(align=True)
        # col.operator(ButtonOperator.bl_idname, text="Change Location", icon="CONSOLE")
        
        # col.operator(ChangeViewpointOperator.bl_idname, text="Change ViewPoint", icon="CONSOLE")
