import bpy

from bpy.types import Operator

class CD_OT_Apply_All_Op(Operator):
    bl_idname = "object.apply_all_mods"
    bl_label = "bpy.data.scenes.keys()"
    bl_description = "Apply all operators of the active object"

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode == "OBJECT":
                return True

        return False

    def execute(self, context):
        
        # Apply all modifiers of active object
        active_obj = context.view_layer.objects.active

        for mod in active_obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=mod.name)

        return {'FINISHED'}


class CD_OT_Cancel_All_Op(Operator):
    bl_idname = "object.cancel_all_mods"
    bl_label = "bpy.data.scenes.keys()"
    bl_description = "Cancel all operators of the active object"

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode == "OBJECT":
                return True

        return False

    def execute(self, context):
        
        # Apply all modifiers of active object
        active_obj = context.view_layer.objects.active

        active_obj.modifiers.clear()

        return {'FINISHED'}