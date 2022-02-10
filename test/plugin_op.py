from multiprocessing.sharedctypes import Value
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
            ('CHANGE_VIEW', 'change viewport', 'change viewport'),
            ('CONVERT_BONES', 'convert to armature', 'convert to armature'),
            ('BEZIER_SPAWN', 'spawn a straight bezier curve', 'spawn a straight bezier curve')
        ]
    )
    def execute(self, context):
        if self.action == 'LOCATION':
            self.change_location(context=context)
        if self.action == 'CHANGE_VIEW':
            self.change_viewport(context=context)
        if self.action == 'CONVERT_BONES':
            self.bone_creator(context=context)
        if self.action == 'BEZIER_SPAWN':
            self.bezier_spawn(context=context)
        return {'FINISHED'}

    @staticmethod
    def change_location(context):
        bpy.context.active_object.location = (0, 0, 0)
        return {'FINISHED'}
        
    @staticmethod
    def change_viewport(context):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D': 
                ctx = {
                    "window": bpy.context.window, 
                    "area": area, # Only change on window currently open
                }
                bpy.ops.view3d.view_axis(ctx, type='RIGHT', align_active=False)
                bpy.context.space_data.region_3d.update()
        return {'FINISHED'}

    @staticmethod
    def bezier_spawn(context):
        bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=True,scale=(0, 0, 0))
        bpy.ops.object.mode_set(mode='EDIT')
        # bpy.ops.object.select_all(action='DESELECT')
        # bezier_curves = bpy.context.view_layer.objects.active
        #https://blender.stackexchange.com/questions/145857/how-do-i-apply-delta-transforms-to-normal-transform
        for obj in bpy.context.selected_objects:
            obj.delta_scale = (1,0,1)
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

    @staticmethod
    def bone_creator(context):
        # context = bpy.context
        # arm_base = context.object
        # bone_base = arm_base.data
        obj = bpy.context.view_layer.objects.active
        #checks to see if selected object is a bezier curve
        if (obj.type == "CURVE"):
            #convert to mesh
            bpy.ops.object.convert(target='MESH', keep_original=True)
            #add skin modifier armature to mesh
            obj.hide_set(True)
            obj = bpy.context.view_layer.objects.active
            bpy.ops.object.modifier_add(type='SKIN')
            bpy.ops.object.skin_armature_create(modifier='Skin')
            #hide bezier curve in mesh state after creation
            obj.hide_set(True)
            # show octagonal shape of bones
            created_bones = bpy.context.view_layer.objects.active
            bpy.data.armatures[created_bones.name].display_type = 'OCTAHEDRAL'
            # bpy.ops.object.mode_set(mode='EDIT')
            # bpy.ops.armature.select_all(action='SELECT')
            # bpy.ops.armature.dissolve()
            bpy.context.space_data.region_3d.update()

            #https://www.youtube.com/watch?v=mGsRmAq9mNU&ab_channel=StevenScott

        return {'FINISHED'}
