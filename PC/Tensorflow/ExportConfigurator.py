#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Import

# In[ ]:


import os
from shutil import copyfile

from ObjectDetection import *


# # Functions

# In[ ]:


########################################################################################
def add_export_module(path):
    
    EXPORT_SCRIPT_SRC = os.path.join(object_detection_path(), "export_inference_graph.py")
    EXPORT_SCRIPT_DST = os.path.join(path, "export_inference_graph.py")
    
    with open(EXPORT_SCRIPT_DST, "w") as dst:
        dst.write("from ObjectDetection import *\n")
        
        # open read only
        with open(EXPORT_SCRIPT_SRC, "r") as src:
            dst.write(src.read())
            
########################################################################################
def gen_export_bat(work_dir, config_path):
    
    BAT_FILE = os.path.join(work_dir, "export.bat")
    TRAIN_SCRIPT_PATH = os.path.join(object_detection_path(), "legacy", "train.py")

    
    CMD = "python export_inference_graph.py "
    CMD += "--input_type image_tensor "
    CMD += "--pipeline_config_path {} "
    CMD += "--trained_checkpoint_prefix training/model.ckpt-XXXX "
    CMD += "--output_directory export"
    
    CMD = CMD.format(config_path)
    with open(BAT_FILE, "w") as file: file.write(CMD)


# # Variables

# In[ ]:


WORK_DIR = "WORK_DIR"
CONFIG_FILE = "CONFIG_FILE"

TRAINING_DIR = os.path.join(WORK_DIR, "training")
CONFIG_DST = os.path.join(TRAINING_DIR, CONFIG_FILE)

EXPORT_DIR = os.path.join(WORK_DIR, "export")

LABELMAP_SRC = os.path.join(TRAINING_DIR, "train.pbtxt")
LABELMAP_DST = os.path.join(EXPORT_DIR, "labelmap.pbtxt")


# # Build files

# In[ ]:


add_export_module(WORK_DIR)
gen_export_bat(WORK_DIR, CONFIG_DST)


# # Add labelmap

# In[ ]:


copyfile(LABELMAP_SRC, LABELMAP_DST)

