import bpy
import bmesh
import struct
from bpy.types import Panel, Operator

#---------------------------------
#FileOpener and selector
#---------------------------------

#will contain the file from CustomDrawOperator for CustomGraphOperator
global file
class CustomDrawOperator(bpy.types.Operator):
    bl_idname = "object.custom_opener"
    bl_label = "Import"
 
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
 
    my_float = bpy.props.FloatProperty(name="Float")
    my_bool = bpy.props.BoolProperty(name="Toggle Option")
    my_string = bpy.props.StringProperty(name="String Value")
 
    def execute(self, context):
        print()
        global file
        file=open(self.filepath, 'r')
        return {'FINISHED'}
 
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
 
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Custom Interface!")
 
        row = col.row()
        row.prop(self, "my_float")
        row.prop(self, "my_bool")
 
        col.prop(self, "my_string")
def register():
    bpy.utils.register_class(CustomDrawOperator)
def unregister():
    bpy.utils.unregister_class(CustomDrawOperator)