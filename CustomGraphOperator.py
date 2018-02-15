import bpy
import bmesh
import struct
import linecache
from math import radians
from bpy.types import Panel, Operator 
from create_custom_graph.ObjectCreator import Obj
#---------------------------------
#FileOpener and selector
#---------------------------------
#will contain the file from CustomDrawOperator for CustomGraphOperator
global file         #Global variable of the selected file

class FileOpener(bpy.types.Operator):
    bl_idname = "object.custom_opener"
    bl_label = "Import"
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    my_float = bpy.props.FloatProperty(name="Float")
    my_bool = bpy.props.BoolProperty(name="Toggle Option")
    my_string = bpy.props.StringProperty(name="String Value")
       
    def execute(self, context):
        print()
        global file
        file=self.filepath         
        return {'FINISHED'}
 
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
 
    def draw(self, context):
        layout = self.layout
        col = layout.column()

#--------------------------------------------------
#Custom Operator to make Graph in 3D from csv file
#--------------------------------------------------
class Custom3DGraph(bpy.types.Operator):
    bl_idname = "object.custom_cubegraph"
    bl_label = "Import"
    
    #Will use raw data file to create uvsphere and place them
    def graphGenerator3D(self):
      
      nbLine=0 #Number of line in the selected file
      #Table for the rows of x,y,z
      tabX=[]
      tabY=[]
      tabZ=[]
      
      objectList=[] #List of objects who will contain the x,y,z location
      
      i=2 #Start at 2 to avoid the header line
      #Position of the cursor in the line for each list 
      px=1
      pz=1
      done=True #Boolean to see if the loop stock the header line in tabX
      f=open(file,'r')
      nbColumn=len(linecache.getline(file,1).split(";"))
      #Stock all the data into lists to create a list of Object 
      while pz<nbColumn :
        i=2
        if done:
          for line in f:
          #get the title of each columns in tabX except for the first one
            while px<nbColumn and done:
              tabX.append(linecache.getline(file,1).split(";")[px])
              px=px+1                        
              #to get the number of object we have to create
            nbLine=nbLine+1
        while i<(nbLine+1):
          #get the first columns variable except for the first one int tabY
          tabY.append(linecache.getline(file,i).split(";")[0])
          #get the columns variable into tabZ maximum 4 per file !
          tabZ.append(linecache.getline(file,i).split(";")[pz])
          i=i+1            
        done=False
        pz=pz+1
      
      x=0
      y=0
      z=0
      i=0
      #create a list of Obj from the 3 table X,Y,Z 
      while i<((nbLine-1)*(nbColumn-1)): #Substract 1 to nbColumn to avoid the first column
        if y==(nbLine-1):
          y=0
          x=x+1
        #check if there is no empty string in the tabZ[]
        if tabZ[i]=="":
          z=-1
        if (',' in tabZ[i]) :  
          z=float(tabZ[i].replace(',','.'))
        if ('.' in tabZ[i]) :
          z=float(tabZ[i])           
        objectList.append(Obj(tabX[x], tabY[i], z))    
        y=y+1
        i=i+1
      i=0
      a=0
      y=0
      xColumn=True
      yColumn=True
      for b in range(nbColumn):
        while i<((nbLine-1)*a) : 
          objNameA=objectList[i].nameA
          x=objectList[i].nameB
          z=objectList[i].z
          bpy.ops.mesh.primitive_cube_add(radius   = 0.5,location = (a*1.85,y * 1.2,(z/1000)/2))       
          # X = current sale's index with a small gap
          # Y = 0. All cubes are aligned in a straight line along the X axis.
          # Z = half the height)            
          cube = bpy.context.object
          cube.dimensions.z = z/1000
          if i<(nbLine-1):
            objNameB=objectList[i].nameB
            bpy.ops.object.text_add(
            location = ( -2 , y*1.2, 0 )
            )
            text = bpy.context.object
            text.rotation_euler.z = radians(0) # Rotate text by 90 degrees along Z axis
            text.data.extrude     = 0.05        # Add depth to the text
            text.data.bevel_depth = 0.01        # Add a nice bevel effect to smooth the text's edges
            text.data.body = objNameB # Set the text to be the columns from tabX[]
          if xColumn:
            bpy.ops.object.text_add(
            location = ( a*1.85 , -2, 0 )
            )
            text = bpy.context.object
            text.rotation_euler.z = radians(270) # Rotate text by 90 degrees along Z axis
            text.data.extrude     = 0.05        # Add depth to the text
            text.data.bevel_depth = 0.01        # Add a nice bevel effect to smooth the text's edges
            text.data.body = objNameA # Set the text to be the columns from tabX[]
          xColumn=False
          i=i+1
          y=y+1

          group_name = objNameA
          if group_name in bpy.data.groups:
            group = bpy.data.groups[group_name]
          else:
            group = bpy.data.groups.new(group_name)
          if not cube.name in group.objects:
                group.objects.link(cube)
        y=0
        xColumn=True
        a=a+1

        
      f.close()
    def execute(self,context):
        self.graphGenerator3D()
        return {'FINISHED'}
#------------------------------------------------------
#Custom Operator to make Graph of sphere from csv file
#------------------------------------------------------  
class CustomSphereGraphOperator(bpy.types.Operator):
    bl_idname = "object.custom_sphere"
    bl_label = "Import"
    
    #Will use raw data file to create uvsphere and place them
    def graphGenerator(self):
        f=open(file,'r')
                
        #For each line will create a sphere and place it
        for line in f: 
            objName,strX,strY,strZ=line.split(";")
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
        self.graphGenerator()
        return {'FINISHED'}



def register():
    bpy.utils.register_class(FileOpener)
    bpy.utils.register_class(CustomSphereGraphOperator)
    bpy.utils.register_class(Custom3DGraph)
    
def unregister():
    bpy.utils.unregister_class(FileOpener)
    bpy.utils.unregister_class(CustomSphereGraphOperator)
    bpy.utils.unregister_class(Custom3DGraph)
     
