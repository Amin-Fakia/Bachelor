# project the uv
# Bake with diffuse (only color) Target Image Textures


    
#bake_uv_to_vc("Untitled")
# import bpy

import subprocess
import sys
import os
import numpy as np

import subprocess
import sys
import os

import time

# from bpy.props import StringProperty, BoolProperty
# from bpy_extras.io_utils import ImportHelper
# from bpy.types import Operator
# from io_mesh_ply import import_ply


def bake_uv_to_vc(i):
    print("backing")
    obj = bpy.context.active_object
    image = bpy.data.images.get("Untitled.002");
    bpy.context.view_layer.objects.active = obj
    bpy.context.scene.render.bake.margin = 0
    bpy.context.scene.render.bake.use_pass_direct = False
    bpy.context.scene.render.bake.use_pass_emit = False
    bpy.context.scene.render.bake.use_pass_indirect = False

    bpy.context.scene.render.bake.use_pass_glossy = False
    bpy.context.scene.render.bake.use_pass_transmission = False
    bpy.context.scene.cycles.samples = 1
    bpy.data.scenes[0].render.engine = "CYCLES"
    bpy.context.preferences.addons[
        "cycles"
    ].preferences.compute_device_type = "CUDA"
    bpy.context.scene.cycles.device = "GPU"
    bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'})
    bpy.ops.object.delete()
    image.save_render(f"F:/EEG_{i}.png")
    bpy.ops.object.select_all(action='DESELECT')
def Project_Ply():
    selection = bpy.context.selected_objects
    print("projecting")
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
    
def execute():
    """Do something with the selected file(s)."""
    
    #filename = os.path.splitext(self.filepath)
    
    filepath = 'C:\\Users\\ameen\\Desktop\\Bachelor_Arbeit\\Bachelor\\mainPy\\ply_data\\'
    c = 0
    if(os.path.exists(filepath + "EEG_0.ply")):

        while True:
            
            file = os.path.join(filepath,f"EEG_{c}.ply")

            Project_Ply()
            bake_uv_to_vc(c)
            if(c>20):
                break
            time.sleep(4)
            c+=1
        
        



execute()
        