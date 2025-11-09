bl_info = {
    "name": "Select by Material",
    "author": "Hesli Reiling",
    "version": (1, 6, 0),
    "blender": (4, 0, 0),
    "location": "Properties > Material > Material Slot Context Menu (Right-click)",
    "description": "Adds a right-click menu option to select all mesh objects using a specific material.",
    "warning": "Requires Blender 4.0 or newer. Context menu may change in dev builds.",
    "doc_url": "https://github.com/HesliGIT/SelectByMaterial",
    "category": "Object",
}

import bpy
from .operator import OBJECT_OT_select_by_material, draw_menu_item

classes = (
    OBJECT_OT_select_by_material,
)

context_menu_class = None

def get_context_menu_class():
    if hasattr(bpy.types, "UI_MT_list_item_context_menu"):
        return bpy.types.UI_MT_list_item_context_menu
    elif hasattr(bpy.types, "UI_MT_button_context_menu"):
        return bpy.types.UI_MT_button_context_menu
    elif hasattr(bpy.types, "WM_MT_button_context"):
        return bpy.types.WM_MT_button_context
    elif hasattr(bpy.types, "UI_MT_template_list_context_menu"):
        return bpy.types.UI_MT_template_list_context_menu
    else:
        return None

def register():
    global context_menu_class
    
    for cls in classes:
        bpy.utils.register_class(cls)
    
    context_menu_class = get_context_menu_class()
    
    if context_menu_class:
        context_menu_class.append(draw_menu_item)
    else:
        print("Select by Material Addon: Could not find a valid context menu class to append to.")


def unregister():
    global context_menu_class
    
    if context_menu_class:
        try:
            context_menu_class.remove(draw_menu_item)
        except (AttributeError, ValueError, TypeError):
            pass
            
    context_menu_class = None

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()