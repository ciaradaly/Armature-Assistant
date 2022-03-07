from distutils.log import error
from os import stat
from pickle import TRUE
import bpy
import mathutils
import numpy as np
import math

from mathutils import Vector

from bpy.types import Operator
from bpy.props import EnumProperty

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#Singular value decomposition
#https://stackoverflow.com/questions/2298390/fitting-a-line-in-3d
def calculate_scd(mesh):
    vec = [(mesh.matrix_world @ v.co) for v in mesh.data.vertices]
    f = np.zeros((3,len(vec)))
    for j in range(3):
        for i in range(len(vec)):
            if j == 0:
                f[j][i] = mathutils.Vector(vec[i]).x
            if j == 1:
                f[j][i] = mathutils.Vector(vec[i]).y
            if j == 2:
                f[j][i] = mathutils.Vector(vec[i]).z
    data = np.concatenate((f[0][:, np.newaxis], f[1][:, np.newaxis], f[2][:, np.newaxis]), axis=1)
    datamean = np.average(data, axis=0)
    uu, dd, vv = np.linalg.svd(data - datamean)
    linepts = vv[0] * np.mgrid[-6:6:2j][:, np.newaxis]
    linepts += datamean
    return linepts
    
def add_bezier(v0 , v1):
    o = (v1 + v0) / 2  
    bpy.ops.curve.primitive_bezier_curve_add()
    curve = bpy.context.view_layer.objects.active
    # bpy.data.curves[bezCurve.name].splines[0].bezier_points[0].co
    spline = bpy.data.curves[curve.name].splines[0]
    bp0 = spline.bezier_points[0]
    bp0.co = v0 - o
    bp0.handle_left_type = bp0.handle_right_type = 'AUTO'

    # spline.bezier_points.add(count=1)
    bp1 = spline.bezier_points[1]
    bp1.co = v1 - o
    bp1.handle_left_type = bp1.handle_right_type = 'AUTO'
    ob = bpy.data.curves.new('CURVE', curve)
    ob.matrix_world.translation = o
    return ob

#Operates button functionalities on UI panel
class ButtonOperator(Operator):
    bl_idname = "object.button_operator"
    bl_label = "Button"
    #https://gist.github.com/AzureDVBB/0b3d941a719e88574533da45d4970492
    action: EnumProperty(
        items=[
            ('LOCATION', 'change location', 'change location'),
            ('VIEW_TOP', 'view top', 'view top'),
            ('VIEW_SIDE', 'view side', 'view side'),
            ('VIEW_FRONT', 'view front', 'view front'),
            ('CONVERT_BONES', 'convert to armature', 'convert to armature'),
            ('BEZIER_SPAWN', 'spawn a straight bezier curve', 'spawn a straight bezier curve'),
            ('BONE_FREQ', 'change bone frequency', 'change bone frequency'),
            ('AUTO_RIG', 'Automatically rig bones to mesh', 'Automatically rig bones to mesh')
        ]
    )
    def execute(self, context):
        if self.action == 'LOCATION':
            self.change_location(context=context)
        if self.action == 'VIEW_TOP':
            self.change_view(view="TOP")
        if self.action == 'VIEW_SIDE':
            self.change_view(view="FRONT")
        if self.action == 'VIEW_FRONT':
            self.change_view(view="RIGHT")
        if self.action == 'CONVERT_BONES':
            self.bone_creator(context=context)
        if self.action == 'BEZIER_SPAWN':
            self.bezier_spawn(context=context)
        if self.action == 'BONE_FREQ':
            self.curve_control(context=context, self=self)
        if self.action == 'AUTO_RIG':
            self.auto_rig(context=context, self=self)
        return {'FINISHED'}

    @staticmethod
    def change_location(context):
        #Must have armature and mesh OBJECT selected
        # Get location of points of mesh and perform Singular Value Decomposition
        for obj in bpy.context.selected_objects:
            if (obj.type == "CURVE"):
                bezCurve = obj
            if (obj.type == 'MESH'):
                mesh = obj
        vectors = calculate_scd(mesh)
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        help1= bpy.context.view_layer.objects.active
        point1= Vector((vectors[0][0],vectors[0][1],vectors[0][2]))
        help1.location = point1
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        help2= bpy.context.view_layer.objects.active
        point2= Vector((vectors[1][0],vectors[1][1],vectors[1][2]))
        help2.location = point2
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.get(bezCurve.name)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True, properties=True)
        #Take bezier curve end and beginning points and move their location to the generated vector points
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.de_select_first()
        bpy.ops.curve.de_select_last()
        bpy.ops.curve.dissolve_verts()
        print(point1)
        bpy.data.curves[bezCurve.name].splines[0].bezier_points[0].co = point1 
        bpy.data.curves[bezCurve.name].splines[0].bezier_points[1].co = point2
        bpy.ops.curve.select_all(action='SELECT')
        #This straightens out the curve
        bpy.ops.curve.handle_type_set(type='VECTOR')
        bpy.ops.curve.handle_type_set(type='ALIGNED')
        bpy.context.space_data.region_3d.update()
        bpy.ops.object.mode_set(mode='OBJECT')
        # bezCurve.data.splines[0].bezier_points[0].location = point2.location
        
        return {'FINISHED'}
        
    @staticmethod
    #Changes view when pressed
    def change_view(view):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D': 
                ctx = {
                    "window": bpy.context.window, 
                    "area": area, # Only change on window currently open
                }
                bpy.ops.view3d.view_axis(ctx, type=view, align_active=False)
                bpy.context.space_data.region_3d.update()
        return {'FINISHED'}

    @staticmethod
    #Spawns in a 'Straight' Bezier Curve at position (0,0,0) for ease of manipulation
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
    #What it says on the tin: creates armature out of a using a bezier curve as a base
    def bone_creator(context):
        try:
            context = bpy.context
            # arm_base = context.object
            # bone_base = arm_base.data
            curve = bpy.context.view_layer.objects.active
            #checks to see if selected object is a bezier curve
            if (curve.type == "CURVE"):
                #convert to mesh
                bpy.ops.object.convert(target='MESH', keep_original=True)
                #add skin modifier armature to mesh
                # curve.hide_set(True)
                obj = bpy.context.view_layer.objects.active
                bpy.ops.object.modifier_add(type='SKIN')
                bpy.ops.object.skin_armature_create(modifier='Skin')
                #hide bezier curve in mesh state after creation
                obj.hide_set(True)
                # show octagonal shape of bones
                created_bones = bpy.context.view_layer.objects.active
                bpy.data.armatures[created_bones.name].display_type = 'OCTAHEDRAL'
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.armature.select_all(action='SELECT')
                bpy.ops.armature.dissolve()
                bpy.context.space_data.region_3d.update()
                bpy.ops.object.mode_set(mode='POSE') 
                # https://github.com/amasawarasen/AmasawaTools/blob/master/amasawaTools_1_5_4.py
                bpy.ops.pose.group_deselect()
                if(len(created_bones.data.bones)-1!=0):
                    boneName = str(len(created_bones.data.bones)-1)
                    myPoseBone = bpy.data.objects[created_bones.name].pose.bones['Bone.00'+boneName]
                else :
                    myPoseBone = bpy.data.objects[created_bones.name].pose.bones['Bone.00']
                bpy.context.object.data.bones.active = myPoseBone.bone
                myPoseBone.bone.select_tail = True
                bpy.context.space_data.region_3d.update()
                #Sets the curve as a constraint using Spline IK. This allows the curve to manipulate
                #The armature. Can increase or decrease the influence if wanted.
                const = myPoseBone.constraints.new("SPLINE_IK")
                const.target = curve
                const.influence = 0.85
                const.chain_count = len(created_bones.data.bones)
                bpy.ops.object.mode_set(mode='OBJECT') 
                bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.get(created_bones.name)
                #Process based on https://www.youtube.com/watch?v=mGsRmAq9mNU&ab_channel=StevenScott
        except:
                ShowMessageBox('Please select a curve', "WARNING", 'ERROR')
        return {'FINISHED'}

    #Changes the amount of bones that appear on the curve
    @staticmethod
    def curve_control(self, context):
        props = self.properties
        scene = context.scene
        amount_of_bones = scene.Bones
        obj = bpy.context.view_layer.objects.active
        #Maybe update this not to require curve? But use curve if its selected.
        if (obj.type == "ARMATURE"):
            created_bones = bpy.context.view_layer.objects.active
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.dissolve()
            if amount_of_bones > 0:
                bpy.ops.armature.subdivide(number_cuts=amount_of_bones-1)
            bpy.ops.object.mode_set(mode='POSE')
            for num in range(len(created_bones.data.bones)):
                if num > 0:
                    #three letter format is f'{num:03}'
                    current_bone = bpy.data.objects[created_bones.name].pose.bones['Bone.'+str(f'{num:03}')].constraints
                    cst = len(current_bone)
                    if(cst>0):
                        for c in current_bone:
                            current_bone.remove(c)
                else :
                    first_bone = bpy.data.objects[created_bones.name].pose.bones['Bone.00'].constraints
                    cst = len(first_bone)
                    if(cst>0):
                        for c in first_bone:
                            first_bone.remove(c)
                
            # bpy.data.objects[created_bones.name].pose.bones['Bone.00'].constraints
            bpy.ops.pose.group_deselect()
            if(len(created_bones.data.bones)!=1):
                myPoseBone = bpy.data.objects[created_bones.name].pose.bones['Bone.001']
            else :
                myPoseBone = bpy.data.objects[created_bones.name].pose.bones['Bone.00']
            bpy.context.object.data.bones.active = myPoseBone.bone
            myPoseBone.bone.select = True
            bpy.context.space_data.region_3d.update()
            const = myPoseBone.constraints.new("SPLINE_IK")
            const.target = bpy.context.scene.objects["BezierCurve"]
            const.influence = 0.85
            const.chain_count = len(created_bones.data.bones)
            bpy.ops.object.mode_set(mode='OBJECT') 
            bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.get(created_bones.name)
        return {'FINISHED'}

    @staticmethod
    def auto_rig(self, context):
        try:
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE':
                    bones = obj
                if obj.type == 'MESH':
                    mesh = obj
            bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.get(bones.name)
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')
            bpy.context.space_data.region_3d.update()
        except:
            ShowMessageBox('Please select created armature and mesh you wish to rig', "WARNING", 'ERROR')
        return {'FINISHED'}
