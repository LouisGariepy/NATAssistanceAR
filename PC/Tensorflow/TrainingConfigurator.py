#!/usr/bin/env python
# coding: utf-8

# -------------------------
# ### Author: Anthony Melin
# ### Date: 2019 August 14
# -------------------------

# # Import

# In[ ]:


import os
from shutil import copyfile, move
from PIL import Image
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf

from ObjectDetection import *

from utils import dataset_util


# # Define functions and classes
# ### Build labelmap file
# Labelmap files provide the associated name object to an index.

# In[ ]:


########################################################################################
def newLabelmapItem(index, name):

    item  = "item {\n"
    item += "    id: {}\n".format(index)
    item += "    name: '{}'\n".format(name)
    item += "}\n"

    return item

############################################################################################
class Labelmap:
    
    ########################################################################################
    def __init__(self, filename_src, filename_dst=None):
        
        self.filename_src = filename_src
        
        if filename_dst == None:
            filename_dst = filename_src.replace(".txt", ".pbtxt")
        self.filename_dst = filename_dst
        
    
    ########################################################################################
    def GetCategories(self):

        with open(self.filename_src, "r") as file:
            self.categories = file.read().split('\n')
            self.categories.remove("")

        return self.categories
    
    ########################################################################################
    def Build(self):

        with open(self.filename_dst, "w") as file:
            
            for i, category in enumerate(self.GetCategories()):
                item = newLabelmapItem(i+1, category)
                file.write(item)


# ## Exporting data to TFRecord
# TFRecord is a file format where all data are stored including both images and annotations.
# #### Get annotations from a directory

# In[ ]:


########################################################################################
class Annotation(dict):
    
    ####################################################################################
    def __init__(self, filename, classes):
        
        self["filename"] = filename
        self.classes = classes
        
        
    ####################################################################################
    def SetArrays(self):
        
        self["indexes"] = []
        self["classes"] = []
        self["xmins"] = []
        self["ymins"] = []
        self["xmaxs"] = []
        self["ymaxs"] = []
        
    
    ####################################################################################
    def AppendLine(self, line):
        
        index, center_x, center_y, width, height = line.split(" ")
    
        self["indexes"].append(int(index)+1)
        self["classes"].append(self.classes[int(index)].encode())
        self["xmins"].append(float(center_x)-float(width)/2)
        self["ymins"].append(float(center_y)-float(height)/2)
        self["xmaxs"].append(float(center_x)+float(width)/2)
        self["ymaxs"].append(float(center_y)+float(height)/2)
        
        
    ####################################################################################
    def Build(self):
        
        self["image_name"] = self["filename"].replace(".txt",".jpg")
        self["image_format"] = b"jpg"
        self["width"], self["height"] = Image.open(self["image_name"]).size
        
        with open(self["image_name"], "rb") as f:
            self["encoded_jpg"] = f.read()
        
        with open(self["filename"], "r") as file:
            lines = filter(None, file.read().split('\n'))
            
        self.SetArrays()
        for line in lines:
            self.AppendLine(line)
    


########################################################################################
def IsAnnotationFile(filename):
    
    if filename.endswith(".txt") and filename != "classes.txt":
        return True
    else:
        return False
    
    
########################################################################################
def GetAnnotationFilenames(path):
    
    return [os.path.abspath(os.path.join(path, filenames)) for filenames in os.listdir(path) if IsAnnotationFile(filenames)]


########################################################################################
def BuildAnnotationList(path, classes):
    
    annotationList = []
    for filename in GetAnnotationFilenames(path):
        annotation = Annotation(filename, classes)
        annotation.Build()
        annotationList.append(annotation)
        
    return annotationList


# #### Writing .record (TFRecord) file

# In[ ]:


########################################################################################
def WriteTFRecord(filename, annotations):
    
    with tf.python_io.TFRecordWriter(filename) as writer:
        
        for annotation in annotations:

            features = tf.train.Features(feature={
                'image/height': dataset_util.int64_feature(annotation["height"]),
                'image/width': dataset_util.int64_feature(annotation["width"]),
                
                'image/filename': dataset_util.bytes_feature(annotation["filename"].encode()),
                'image/source_id': dataset_util.bytes_feature(annotation["filename"].encode()),
                'image/encoded': dataset_util.bytes_feature(annotation["encoded_jpg"]),
                'image/format': dataset_util.bytes_feature(annotation["image_format"]),

                'image/object/bbox/xmin': dataset_util.float_list_feature(annotation["xmins"]),
                'image/object/bbox/xmax': dataset_util.float_list_feature(annotation["xmaxs"]),
                'image/object/bbox/ymin': dataset_util.float_list_feature(annotation["ymins"]),
                'image/object/bbox/ymax': dataset_util.float_list_feature(annotation["ymaxs"]),
                'image/object/class/text': dataset_util.bytes_list_feature(annotation["classes"]),
                'image/object/class/label': dataset_util.int64_list_feature(annotation["indexes"]),
            })

            writer.write(tf.train.Example(features=features).SerializeToString())


# ## Download model
# If it was not already used, the object detector directory will be downloaded on the tensorflow download base. The directory provide a config file to use for the training.

# In[ ]:


########################################################################################
def extract(model_name, target_dir):
    
    MODEL_ZIPFILE = model_name + '.tar.gz'
    MODEL_PATH = os.path.join("cnn", MODEL_ZIPFILE)
    
    tar_file = tarfile.open(MODEL_PATH)
    for file in tar_file.getmembers():
        tar_file.extract(file, target_dir)
        

########################################################################################
def download(model_name):
    
    DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
    MODEL_ZIPFILE = model_name + '.tar.gz'
    MODEL_URL = DOWNLOAD_BASE + MODEL_ZIPFILE
    
    opener = urllib.request.URLopener()
    opener.retrieve(MODEL_URL, MODEL_ZIPFILE)
    opener.cleanup()
    opener.close()
    

########################################################################################
def need_to_download(model_name):
    
    MODEL_ZIPFILE = model_name + '.tar.gz'
    
    if MODEL_ZIPFILE not in os.listdir("cnn"):
        return True
    else:
        return False
        

########################################################################################
def move_to_cnn_dir(model_name):

    SRC = model_name + '.tar.gz'
    DST = os.path.join("cnn", model_name + '.tar.gz')
    move(SRC, DST)
    
    
########################################################################################
def download_if_needed(model_name):
    
    if need_to_download(model_name):
        download(model_name)
        move_to_cnn_dir(model_name)


# ## Complete the .config file
# The .config file set the trainning by specify parameters like loss function or number of evaluation to do. Path to train and test tfrecord file must be completed.

# In[ ]:


########################################################################################
def complete_val(lines, param, val, start):
    
    for i in range(start, len(lines)):
        
        if param in lines[i] :
            lines[i] = param + ': ' + val
            return i+1
        
    return i+1

########################################################################################
def complete_values(path, parameters):
    
    # read the file to get its lines
    with open(path) as file:
        lines = file.read().split("\n")
    
    # loop over lines for setting parameters
    i = 0
    for param, value in parameters:
        
        if type(value) == str:
            val = '"{}"'.format(value.replace("\\", "/")) # backslash must be replace in config file and " inserted
        elif type(value) == bool:
            val = str(value).lower()
        else:
            val = str(value)
        
        i = complete_val(lines, param, val, i)
        if i == len(lines): break
            
    # update the file
    with open(path, "w") as file:
        for line in lines:
            file.write(line+"\n")


# # Add scripts

# In[ ]:


########################################################################################
def add_train_module(path):
    
    TRAIN_SCRIPT_SRC = os.path.join(object_detection_path(), "legacy", "train.py")
    TRAIN_SCRIPT_DST = os.path.join(path, "train.py")
    
    with open(TRAIN_SCRIPT_DST, "w") as dst:
        dst.write("from ObjectDetection import *\n")
        
        # open read only
        with open(TRAIN_SCRIPT_SRC, "r") as src:
            dst.write(src.read())
            

########################################################################################
def gen_train_bat(work_dir, training_dir, config_path):
    
    BAT_FILE = os.path.join(work_dir, "train.bat")
    TRAIN_SCRIPT_PATH = os.path.join(object_detection_path(), "legacy", "train.py")

    CMD = "python train.py --logtostderr --train_dir={} --pipeline_config_path={}".format(training_dir, config_path)
    with open(BAT_FILE, "w") as file: file.write(CMD)
        


# # Main
# ## Variables

# In[ ]:


WORK_DIR = "WORK_DIR"

TRAIN_DIR = os.path.join(WORK_DIR, "train")
TEST_DIR = os.path.join(WORK_DIR, "test")

TRAINING_DIR = os.path.join(WORK_DIR, "training")

MODEL_NAME = "MODEL_NAME"
CONFIG_FILE = "CONFIG_FILE"


# ## Create training directory

# In[ ]:


try:
    os.mkdir(TRAINING_DIR)
except:
    pass


# ## Labelmaps

# In[ ]:


# train filenames
TRAIN_CLASSES = os.path.join(TRAIN_DIR, "classes.txt")
TRAIN_LABELMAP = os.path.join(TRAINING_DIR, "train.pbtxt")

# test filenames
TEST_CLASSES = os.path.join(TEST_DIR, "classes.txt")
TEST_LABELMAP = os.path.join(TRAINING_DIR, "test.pbtxt")

# build labelmaps
train_labelmap = Labelmap(TRAIN_CLASSES, TRAIN_LABELMAP)
train_labelmap.Build()

test_labelmap = Labelmap(TEST_CLASSES, TEST_LABELMAP)
test_labelmap.Build()


# ## TFRecord

# In[ ]:


TRAIN_RECORD = os.path.join(TRAINING_DIR, "train.record")
TEST_RECORD = os.path.join(TRAINING_DIR, "test.record")

train_annotations = BuildAnnotationList(TRAIN_DIR, train_labelmap.GetCategories())
test_annotations = BuildAnnotationList(TEST_DIR, test_labelmap.GetCategories())
    
WriteTFRecord(TRAIN_RECORD, train_annotations)
WriteTFRecord(TEST_RECORD, test_annotations)


# ## Model importation and config
# ### Pretrained model

# In[ ]:


download_if_needed(MODEL_NAME)
extract(MODEL_NAME, TRAINING_DIR)


# ### Config file

# In[ ]:


CONFIG_SRC = os.path.join(object_detection_path(), "samples/configs", CONFIG_FILE)
CONFIG_DST = os.path.join(TRAINING_DIR, CONFIG_FILE)

copyfile(CONFIG_SRC, CONFIG_DST)


# ### Checkpoint file

# In[ ]:


CHECK_FILE = os.path.join(TRAINING_DIR, MODEL_NAME, "model.ckpt")

complete_values(CONFIG_DST, [
                ("num_classes", len(train_labelmap.categories)),
                ("fine_tune_checkpoint", CHECK_FILE),
                ("input_path", TRAIN_RECORD),
                ("label_map_path", TRAIN_LABELMAP),
                ("num_examples", 150),
                ("input_path", TEST_RECORD),
                ("label_map_path", TEST_LABELMAP),
                ("shuffle", True)
                ])


# ## Train files (.py and .bat)

# In[ ]:


# copy object detection initializer module
OBJECT_DETECTION_DST = os.path.join(WORK_DIR, "ObjectDetection.py")
copyfile("ObjectDetection.py", OBJECT_DETECTION_DST)

add_train_module(WORK_DIR)
gen_train_bat(WORK_DIR, TRAINING_DIR, CONFIG_DST)

