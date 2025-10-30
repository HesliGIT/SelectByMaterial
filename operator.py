import bpy
from bpy.types import Operator

class OBJECT_OT_select_by_material(Operator):
    bl_idname = "object.select_by_material"
    bl_label = "Select Objects With This Material"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return (
            obj is not None and
            obj.type == 'MESH' and
            len(obj.material_slots) > 0 and
            obj.active_material_index >= 0
        )

    def execute(self, context):
        active_obj = context.object
        idx = active_obj.active_material_index
        
        if idx < 0 or idx >= len(active_obj.material_slots):
            return {'CANCELLED'}
            
        target_slot = active_obj.material_slots[idx]
        target_mat = target_slot.material

        if not target_mat:
            self.report({'INFO'}, "Selected material slot is empty.")
            return {'CANCELLED'}

        bpy.ops.object.select_all(action='DESELECT')

        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for slot in obj.material_slots:
                    if slot.material == target_mat:
                        obj.select_set(True)
                        break
        
        context.view_layer.objects.active = active_obj
        return {'FINISHED'}

def draw_menu_item(self, context):
    ui_list = getattr(context, "ui_list", None)
    if ui_list and ui_list.bl_idname == "MATERIAL_UL_matslots":
        self.layout.operator(OBJECT_OT_select_by_material.bl_idname)