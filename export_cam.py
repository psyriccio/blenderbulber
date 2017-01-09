import bpyml
import bpy_types
import bpy_extras
import bl_operators
import bl_ui
import bpyml_ui
import sys
import os
import bpy
import mathutils
import math

def get_alpha(vec):
    return math.atan2(vec.y, vec.x)

def get_beta(vec):
    return math.atan2(vec.z, math.sqrt(vec.x * vec.x + vec.y * vec.y))

global_scale = 0.5

tscene = bpy.context.scene
fpath = str(bpy.context.blend_data.filepath.replace(".blend", ".cam"))
os.remove(fpath)
fcam = open(fpath, mode='x', buffering=-1, encoding='UTF-8', errors=None, newline=None, closefd=True)
fcam.write("[frames]\n")
fcam.write("frame;main_camera_x;main_camera_y;main_camera_z;main_target_x;main_target_y;main_target_z;main_camera_top_x;main_camera_top_y;main_camera_top_z\n")
for frmnum in range(tscene.frame_start, tscene.frame_end + 1):
    tscene.frame_set(frmnum)
    objcam = tscene.camera
    objtarget = tscene.objects['CameraTarget']
    eul = objcam.rotation_euler.copy()
    eul.x, eul.y = eul.y, eul.x
    fcam.write(str(frmnum) + ";")
    #fcam.write(str(objcam.location).replace("<Vector ", "").replace(">", "").replace("(", "").replace(")", "").replace(", ", ";"))
    cam_vec = objcam.location
    tar_vec = objtarget.location
    fwd_vec = tar_vec - cam_vec
    fwd_vec.normalize()
    yaw = get_alpha(fwd_vec) - 0.5 * math.pi
    pitch = get_beta(fwd_vec)
    distance = (tar_vec - cam_vec).length
    top_vec = cam_vec.copy()
    top_vec.rotate(eul)
    top_vec = top_vec.reflect(mathutils.Vector((0.0, 1.0, 0.0)))
    top_vec = top_vec.reflect(mathutils.Vector((1.0, 0.0, 0.0)))
    top_vec_tmp = top_vec.normalized()
    fcam.write(str(repr(cam_vec.x * global_scale)) + ";" + str(repr(cam_vec.y * global_scale)) + ";" + str(repr(cam_vec.z * global_scale)) + ";")
    fcam.write(str(repr(tar_vec.x * global_scale)) + ";" + str(repr(tar_vec.y * global_scale)) + ";" + str(repr(tar_vec.z * global_scale)) + ";")
    fcam.write(str(repr(top_vec.x * global_scale)) + ";" + str(repr(top_vec.y * global_scale)) + ";" + str(repr(top_vec.z * global_scale)) + "\n")
fcam.flush()
fcam.close()
