# coding: utf-8

import numpy as np
import cv2
import glm
import base64

def decodeJpeg(js_data):
    
    base64_sequence = js_data[23:]
    jpg_sequence = base64.b64decode(base64_sequence)
    str_sequence = np.frombuffer(jpg_sequence, np.uint8)
    
    return cv2.imdecode(str_sequence, 1)


## Convert a IP adress encoded in byte array of 4 elements to string.
def ipv4_decode(byte_array):
    
    assert len(byte_array) == 4, "byte array length must be 4, got {}".format(len(byte_array))
    
    ip = []
    for i, value in enumerate(byte_array):
        if type(value) == int:
            ip.append(str(value))
        else:
            raise ValueError("element {} may not be byte".format(i))
    return ".".join(ip)


####### FOR SCENARII
## Return the length between two points in 3D space
# @param pos1 and pos2 are glm.vec3 (x, y, z)
def length2D(pos1, pos2):
    
    v1 = glm.vec2(pos1)
    v2 = glm.vec2(pos2)
    
    return glm.length(v2-v1)



## Return the length between two points in 3D space
# @param pos1 and pos2 are glm.vec3 (x, y, z)
def length3D(pos1, pos2):
    
    v1 = glm.vec3(pos1)
    v2 = glm.vec3(pos2)
    
    return glm.length(v2-v1)
