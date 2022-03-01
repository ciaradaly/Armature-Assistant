import bpy

from bpy.types import Panel
from bpy.props import *

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

    
class BASE_panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Blender Plugin"
    # bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}


class OBJECT_PT_ArmatureAssistantPanel(BASE_panel, Panel):
    bl_idname = "OBJECT_PT_ArmatureAssistantPanel"
    bl_label = "Armature Assistant"

    @classmethod
    def poll(self,context):
        return context.object is not None

    bpy.types.Scene.Bones = IntProperty(name="Bones", description="Change bone Frequency using slider", min=0, max=255, default=10)

    def draw(self, context):
        
        layout = self.layout 
        #layout.prop(context.scene, "MyInt", slider=True)
        
        layout.operator('object.button_operator', text="Add new Bezier Curve", icon="CURVE_BEZCURVE").action='BEZIER_SPAWN'
        layout.label(text="Align curve to center of mesh")
        layout.operator('object.button_operator', text="Align", icon="GRID").action='LOCATION'
        layout.label(text="Change Viewpoint:")
        layout.operator('object.button_operator', text="Top", icon="AXIS_TOP").action='VIEW_TOP'
        layout.operator('object.button_operator', text="Side", icon="AXIS_SIDE").action='VIEW_SIDE'
        layout.operator('object.button_operator', text="Front", icon="AXIS_FRONT").action='VIEW_FRONT'
        layout.label(text="Select curve and convert to bone:")
        layout.operator('object.button_operator', text="Bone converter", icon="BONE_DATA").action='CONVERT_BONES'
        layout.label(text="Change amount of bones on armature:")
        layout.prop(context.scene, 'Bones', slider=True, icon='CON_SPLINEIK')
        layout.operator('object.button_operator', text="Change Frequency", icon="GROUP_BONE").action='BONE_FREQ'
        layout.label(text="Select mesh and bone to rig:")
        layout.operator('object.button_operator', text="Rig", icon="ARMATURE_DATA").action='AUTO_RIG'
        # layout.prop(bpy.context.scene, "local_view")
        # layout.operator(ButtonOperator.bl_idname, text="Change Location", icon="CONSOLE")

class OBJECT_PT_InfoPanel(BASE_panel, Panel):
    bl_parent_id = "OBJECT_PT_ArmatureAssistantPanel"
    bl_label = "Information Tab"

    def draw(self, context):
        layout = self.layout
        layout.label(text="1. Spawn Bezier Curve (Either in UI or manually)")
        layout.label(text="2. Select Mesh and curve and use 'align' to center")
        layout.label(text="3. In edit mode, fit curve to mesh")
        layout.label(text="4. Select curve and press Convert to Bone")
        layout.label(text="5. Change amount of bones along curve by changing")
        layout.label(text="slider amount and selecting 'Change Frequency'")
        layout.label(text="6. Select mesh and armature and press Rig")
