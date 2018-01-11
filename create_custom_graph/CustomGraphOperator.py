import bpy
import bmesh
import struct
import CustomDrawOperator
from bpy.types import Panel, Operator
#--------------------------------------------------
#Custom Operator to make Graph from data file
#--------------------------------------------------  
class CustomGraphOperator(bpy.types.Operator):
    bl_idname = "object.custom_draw"
    bl_label = "Import"
    
    #Will use raw data file to create uvsphere and place them
    def a(self):
        f = open("file.raw","r")
        for line in f: 
            objName=line.split()[0]
            strX=line.split()[1]
            strY=line.split()[2]
            strZ=line.split()[3]
            x=float(strX)
            y=float(strY)
            z=float(strZ)
            print(objName," ",x," ",y," ",z)
            bpyscene = bpy.context.scene
            # Create an empty mesh and the object.
            mesh = bpy.data.meshes.new(objName)
            basic_sphere = bpy.data.objects.new(objName, mesh)
            # Add the object into the scene.
            bpyscene.objects.link(basic_sphere)
            bpyscene.objects.active = basic_sphere
            basic_sphere.select = True
            # Construct the bmesh cube and assign it to the blender mesh.
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)
            bm.to_mesh(mesh)
            bm.free()
            bpy.ops.object.modifier_add(type='SUBSURF')
            bpy.ops.object.shade_smooth()
            bpy.data.objects[objName].location.x += x
            bpy.data.objects[objName].location.y += y
            bpy.data.objects[objName].location.z += z
        f.close()
    def execute(self,context):
        self.a()
        return {'FINISHED'}
def register():
    bpy.utils.register_class(CustomGraphOperator)
def unregister():
    bpy.utils.unregister_class(CustomGraphOperator) 