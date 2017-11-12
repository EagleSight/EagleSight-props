import bpy
import struct
import math
import bmesh

def read_some_data(context, filepath):
    f = open(filepath, 'rb')
    data = f.read()
    f.close()
    
    header = struct.unpack('=HHhf', data[0:10])
    
    img_map = bpy.data.images.new(
        name='map', 
        width=header[0], 
        height=header[1], 
        float_buffer=True
    )
    
    width = header[0]
    height = header[1]
    top = float(header[2])
    distance = header[3]
    
    data_counter = 0+2+2+2+4
    
    new_pixels = [0.0, 0.0, 0.0, 1.0] * int(len(img_map.pixels) / 4)
    
    for row in range(height-1, 0, -1): # top->bottom
        for column in range(0, width): # right->left
            v = float(struct.unpack('=h', data[data_counter:data_counter+2])[0])/top
            
            px = (row * width + column) * 4
            
            new_pixels[px] = v
            new_pixels[px+1] = v
            new_pixels[px+2] = v
            data_counter +=  2

    img_map.pixels = new_pixels
    
    # Experimental, we generate the points
    mesh = bpy.data.meshes.new("map")

    bm = bmesh.new()
    
    scale_up = 0.01
    
    pxs = list(img_map.pixels)
    w_center = width / 2
    h_center = height / 2
    scaled_distance = distance * scale_up
    scaled_top = top * scale_up 

    # Set vertices position from pixels of the map texture
    for row in range(height, 0, -1): # top->bottom
        for column in range(0, width): # right->left
            
            i = ((row-1)*width+column)
            
            v = (
                (column - w_center) * scaled_distance, # X
                (row - h_center) * scaled_distance, # Y
                pxs[i*4] * scaled_top # Z
            )
            
            bm.verts.new(v)

    bm.verts.ensure_lookup_table()
    
    for row in range(0, height-1):
        for column in range(0, width-1):
            #    30------2
            #    | \     |
            #    |   \   |
            #    |     \ |
            #    4------51
            
            bm.faces.new((
                bm.verts[row*width+column],      # 0
                bm.verts[(row+1)*width+column+1],# 1
                bm.verts[row*width+column+1]     # 2
            ))
            
            bm.faces.new((
                bm.verts[row*width+column],      # 3
                bm.verts[(row+1)*width+column],  # 4
                bm.verts[(row+1)*width+column+1] # 5
            ))

    bm.to_mesh(mesh)
    mesh.update()


    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportEagleSightMap(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "eaglesight.import_map"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import EagleSight map"

    # ImportHelper mixin class uses this
    filename_ext = ".esmap"

    filter_glob = StringProperty(
            default="*.esmap",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    def execute(self, context):
        return read_some_data(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportEagleSightMap.bl_idname, text="EagleSight map (.esmap)")


def register():
    bpy.utils.register_class(ImportEagleSightMap)
    bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportSomeData)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()


    bpy.ops.eaglesight.import_map('INVOKE_DEFAULT')