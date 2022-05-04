# project the uv
# Bake with diffuse (only color) Target Image Textures


    
#bake_uv_to_vc("Untitled")
import bpy

import subprocess
import sys
import os
import numpy as np

import subprocess
import sys
import os


# path to python.exe


def bake_uv_to_vc(i):
    # Lookup the image by name. Easier than trying to figure out which one is
    # currently active
#    scene = bpy.context.scene
    obj = bpy.context.active_object
    image = bpy.data.images.get("Untitled.002");
    bpy.context.view_layer.objects.active = obj
    bpy.context.scene.render.bake.margin = 0
    bpy.context.scene.render.bake.use_pass_direct = False
    bpy.context.scene.render.bake.use_pass_emit = False
    bpy.context.scene.render.bake.use_pass_indirect = False
    bpy.context.scene.render.bake.use_pass_glossy = False
    bpy.context.scene.render.bake.use_pass_transmission = False
    
    bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'})
    image.save_render(f"F:/EEG_{i}.png")
    print("finished")

from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from io_mesh_ply import import_ply

class OT_TestOpenFilebrowser(Operator, ImportHelper):

    bl_idname = "test.open_filebrowser"
    bl_label = "Open the file browser"
    
    
    path : StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')
        
    some_boolean: BoolProperty(
        name='Do a thing',
        description='Do a thing with the file you\'ve selected',
        default=True,
    )
    def bake_uv_to_vc(self,i):
        obj = bpy.context.active_object
        image = bpy.data.images.get("Untitled.002");
        bpy.context.view_layer.objects.active = obj
        bpy.context.scene.render.bake.margin = 0
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_emit = False
        bpy.context.scene.render.bake.use_pass_indirect = False
        bpy.context.scene.render.bake.use_pass_glossy = False
        bpy.context.scene.render.bake.use_pass_transmission = False
        
        bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'})
        image.save_render(f"F:/EEG_{i}.png")
        bpy.ops.object.select_all(action='DESELECT')
    def Project_Ply(self):
        selection = bpy.context.selected_objects

        # Get the active object
        active_object = bpy.context.active_object
        
        
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:
            # Select each object
            obj.select_set(True)
            # Make it active
            bpy.context.view_layer.objects.active = obj
            # Toggle into Edit Mode
            bpy.ops.object.mode_set(mode='EDIT')
            # Select the geometry
            bpy.ops.mesh.select_all(action='SELECT')
            # Call the smart project operator
            bpy.ops.uv.unwrap()
            mat = bpy.data.materials.get("Material0")
            obj.data.materials.append(mat) 
            # Toggle out of Edit Mode
            bpy.ops.object.mode_set(mode='OBJECT')
            # Deselect the object
            obj.select_set(False)
        
        # Restore the selection
        for obj in selection:
            obj.select_set(True)
        
        # Restore the active object
        bpy.context.view_layer.objects.active = active_object
        
    def execute(self, context):
        """Do something with the selected file(s)."""
        
        #filename = os.path.splitext(self.filepath)
        
        dirname = os.path.dirname(self.filepath)
        ply_files = [f for f in os.listdir(dirname) if f.endswith('.ply')]
        c = 0
        for i in ply_files:
            file = os.path.join(dirname,i)
            ply_file = import_ply.load_ply(file)
            self.Project_Ply()
            self.bake_uv_to_vc(c)
            c+=1
            
            
        
#        print('File name:', filename)
#        print('File extension:', extension)
#        print('Some Boolean:', self.some_boolean)
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OT_TestOpenFilebrowser)


def unregister():
    bpy.utils.unregister_class(OT_TestOpenFilebrowser)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.test.open_filebrowser('INVOKE_DEFAULT')
        