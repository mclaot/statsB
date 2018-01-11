import bpy
import struct
import os
import sys
from bpy.types import Panel, Operator   
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
    "wiki_url": "https://wiki.blender.org/index.php/Extensions:2.6"
                "/Py/Scripts/Object/Add_Advanced",
    "support": "COMMUNITY",
    "category": "Object"}
from create_custom_graph import CustomDrawOperator
from create_custom_graph import CustomGraphOperator

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
        layout.operator("object.custom_opener", text="Load a file")
        layout.operator("object.custom_draw", text="Generate a graph", icon="MESH_UVSPHERE")   
        
def register():
    bpy.utils.register_module(__name__)
def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
