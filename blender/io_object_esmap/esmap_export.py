import bpy
import struct


def write_some_data(context, filepath: str, top_altitude: int, distance: float):

    f = open(filepath, 'wb')

    # TODO: Raise error when image doesn't exist
    map_img = bpy.data.images['map']

    width, height = map_img.size
    
    f.write(struct.pack('=HHhf', w, h, top_altitude, distance))

    pxs = list(map_img.pixels)
    
    # Exports all the points in the texture
    for row in range(height, 0, -1): # top->bottom
        for column in range(0, width): # right->left
            
            # Store the height of the pixels
            f.write(struct.pack('=h', int(pxs[((row-1)*width+column)*4]*top_altitude)))

    f.close()

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, IntProperty, FloatProperty
from bpy.types import Operator


class ExportSomeData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "eaglesight.export_map"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export EagleSight map file"

    # ExportHelper mixin class uses this
    filename_ext = ".esmap"

    filter_glob = StringProperty(
            default="*.esmap",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    top_altitude = IntProperty(
            name="Top Altitude",
            description="Height of the heighest point on the map (in meters)",
            default=1,
            max=9000,
            min=0
            )

    distance = FloatProperty(
            name="Distance",
            description="Distance between points (in meters)",
            default=30.0,
            max=100.0,
            min=0.01
            )



    def execute(self, context):
        return write_some_data(context, self.filepath, self.top_altitude, self.distance)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="EagleSight map (.esmap)")


def register():
    bpy.utils.register_class(ExportSomeData)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportSomeData)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

