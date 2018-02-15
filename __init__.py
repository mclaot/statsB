import bpy
import struct
import os
import sys
from bpy.types import Panel, Operator
from . import CustomGraphOperator
   
#------------------------------------------------------------------------------------ 
#Custom panel with the option to load a selected file and genererate the grah
#------------------------------------------------------------------------------------    
bl_info = {
    "name": "Create Custom graph",
    "author": "Quentel William",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Add ",
    "description": "Add option to genererate graphics",
    "warning": "file must be ",
    "wiki_url": "",
    "support": "COMMUNITY",
    "category": "Object"}
import importlib
if "bpy" in locals():
    importlib.reload(CustomGraphOperator)
else:
    from . import CustomGraphOperator

import bpy    

class GraphOpener(bpy.types.Panel):
    """Creates the Create Object Panel"""
    bl_label = "Create Graph"
    bl_idname = "create_graph"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Graph Maker:"
    
    #Place the button on the Panel
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        layout.operator("object.custom_opener", text="Select a CSV file",icon="FILE_FOLDER")
        layout.operator("object.custom_cubegraph",text="Generate a 3D graph", icon="OBJECT_DATAMODE")
        layout.operator("object.custom_sphere",text="Generate a 3D graph", icon="MATSPHERE")
           
def register():
    bpy.utils.register_module(__name__)
def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
