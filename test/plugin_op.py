from distutils.log import error
from os import stat
from pickle import TRUE
import bpy
import mathutils
import numpy as np

from mathutils import Vector

from bpy.types import Operator
from bpy.props import EnumProperty

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#First Principal Component
#https://stackoverflow.com/questions/2298390/fitting-a-line-in-3d
def calculate_FPC(mesh):
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
    min = f.min()
    max = f.max()
    #min and max were de-commissioned as they were presenting bug issues.
    linepts = vv[0] * np.mgrid[6:-6:2j][:, np.newaxis]
    linepts += datamean
    return linepts

#Operates button functionalities on UI pan
class ButtonOperator(Operator):
    bl_idname = "object.button_operator"
    bl_label = "Button"
    #https://gist.github.com/AzureDVBB/0b3d941a719e88574533da45d4970492
    action: EnumProperty(
        items=[
            ('ALIGN', 'align objects', 'align objects'),
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
        if self.action == 'ALIGN':
            self.align(context=context)
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
    def align(context):
        #Must have armature and mesh OBJECT selected
        #Get location of points of mesh and perform Singular Value Decomposition
        try:
            for obj in bpy.context.selected_objects:
                if (obj.type == "CURVE"):
                    bezCurve = obj
                if (obj.type == 'MESH'):
                    mesh = obj
            vectors = calculate_FPC(mesh)
            point1= Vector((vectors[0][0],vectors[0][1],vectors[0][2]))
            point2= Vector((vectors[1][0],vectors[1][1],vectors[1][2]))
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects[bezCurve.name].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[bezCurve.name]
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True, properties=True)
            #Take bezier curve end and beginning points and move their location to the generated vector points
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.curve.select_all(action='SELECT')
            bpy.ops.curve.de_select_first()
            bpy.ops.curve.de_select_last()
            bpy.ops.curve.dissolve_verts()
            bpy.data.curves[bezCurve.name].splines[0].bezier_points[0].co = point1 
            bpy.data.curves[bezCurve.name].splines[0].bezier_points[1].co = point2
            bpy.ops.curve.select_all(action='SELECT')
            #This straightens out the curve
            bpy.ops.curve.handle_type_set(type='VECTOR')
            bpy.ops.curve.handle_type_set(type='ALIGNED')
            bpy.context.space_data.region_3d.update()
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects[bezCurve.name].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[bezCurve.name]
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            bezCurve.location = mesh.location
        except:
            ShowMessageBox('Ensure MESH and CURVE are selected', "WARNING", 'ERROR')
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
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

    @staticmethod
    #What it says on the tin: creates armature out of a using a bezier curve as a base
    def bone_creator(context):
        context = bpy.context
        curve = bpy.context.view_layer.objects.active
        #checks to see if selected object is a bezier curve
        if (curve.type == "CURVE"):
            #convert to mesh
            bpy.ops.object.convert(target='MESH', keep_original=True)
            #add skin modifier armature to mesh
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
        else:
            ShowMessageBox('Please select a curve', "WARNING", 'ERROR')
        return {'FINISHED'}

    #Changes the amount of bones that appear on the curve
    @staticmethod
    def curve_control(self, context):
        props = self.properties
        scene = context.scene
        amount_of_bones = scene.Bones
        obj = bpy.context.view_layer.objects.active
        if (obj.type == "ARMATURE"):
            created_bones = bpy.context.view_layer.objects.active
            bpy.ops.object.mode_set(mode='EDIT')
            # Iterates through all bones and removes the SPLINE_IK constraint
            for num in range(len(created_bones.data.bones)):
                if num > 0:
                    #three letter format is f'{num:03}'
                    current_bone = bpy.data.objects[created_bones.name].pose.bones['Bone.'+str(f'{num:03}')].constraints
                    cst = len(current_bone)
                    if(cst>0):
                        for c in current_bone:
                            if c.type == "SPLINE_IK":
                                curveBez = c.target
                            current_bone.remove(c)
                else :
                    first_bone = bpy.data.objects[created_bones.name].pose.bones['Bone.00'].constraints
                    cst = len(first_bone)
                    if(cst>0):
                        for c in first_bone:
                            if c.type == "SPLINE_IK":
                                curveBez = c.target
                            first_bone.remove(c)
            #subdividing bones to amount of cuts specified on the slider
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.dissolve()
            if amount_of_bones > 0:
                bpy.ops.armature.subdivide(number_cuts=amount_of_bones-1)
            bpy.ops.object.mode_set(mode='POSE')
            bpy.ops.pose.group_deselect()
            #End bones name is 'Bone.001' is there is more than one bone. Otherwise it is known as 'Bone.00'.
            if(len(created_bones.data.bones)!=1):
                influenceBone = 0.85
                myPoseBone = bpy.data.objects[created_bones.name].pose.bones['Bone.001']
            else :
                influenceBone = 0.95
                myPoseBone = bpy.data.objects[created_bones.name].pose.bones['Bone.00']
            bpy.context.object.data.bones.active = myPoseBone.bone
            myPoseBone.bone.select = True
            bpy.context.space_data.region_3d.update()
            #adding constraint to end bone
            const = myPoseBone.constraints.new("SPLINE_IK")
            const.target = bpy.context.scene.objects[curveBez.name]
            const.influence = influenceBone
            const.chain_count = len(created_bones.data.bones)
            bpy.ops.object.mode_set(mode='OBJECT') 
            bpy.context.view_layer.objects.active = bpy.context.view_layer.objects.get(created_bones.name)
        else:
            ShowMessageBox('Please select created Bones', "WARNING", 'ERROR')
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
