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

this_scene = bpy.context.scene
file_path = str(bpy.context.blend_data.filepath.replace(".blend", ".cam"))
os.remove(file_path)
file_cam_anim = open(file_path, mode='x', buffering=-1, encoding='UTF-8', errors=None, newline=None, closefd=True)
file_cam_anim.write("[frames]\n")
file_cam_anim.write("frame;main_camera_x;main_camera_y;main_camera_z;"
                    "main_target_x;main_target_y;main_target_z;"
                    "main_camera_top_x;main_camera_top_y;main_camera_top_z\n")
for frame_num in range(this_scene.frame_start, this_scene.frame_end + 1):
    this_scene.frame_set(frame_num)
    object_cam = this_scene.camera
    object_target = this_scene.objects['CameraTarget']
    eul = object_cam.rotation_euler.copy()
    eul.x, eul.y = eul.y, eul.x
    file_cam_anim.write(str(frame_num) + ";")
    cam_vec = object_cam.location
    tar_vec = object_target.location
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
    file_cam_anim.write(str(repr(cam_vec.x * global_scale)) + ";" + str(repr(cam_vec.y * global_scale)) + ";" + str(
        repr(cam_vec.z * global_scale)) + ";")
    file_cam_anim.write(str(repr(tar_vec.x * global_scale)) + ";" + str(repr(tar_vec.y * global_scale)) + ";" + str(
        repr(tar_vec.z * global_scale)) + ";")
    file_cam_anim.write(str(repr(top_vec.x * global_scale)) + ";" + str(repr(top_vec.y * global_scale)) + ";" + str(
        repr(top_vec.z * global_scale)) + "\n")
file_cam_anim.flush()
file_cam_anim.close()
