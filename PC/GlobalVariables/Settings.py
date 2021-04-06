import os

#Paths
filedir = os.path.dirname(__file__) #path to Settings.py
projectdir = os.path.join(filedir, os.pardir, os.pardir) #path to NATAssistanceAR/
MODEL_DIRECTORY = os.path.join(projectdir,'ModelsForNAT','model_3')
GRAPH = MODEL_DIRECTORY + "/frozen_inference_graph.pb"
LABELS = MODEL_DIRECTORY + "/labelmap.pbtxt"

NUM_CLASSES = 7

HOST = "192.168.1.11"

#Ports
CAMERA_PORT = 9999
COLLISION_PORT = 9998
ANNOTATION_PORT = 9997

#Keys
EXIT_KEY = "q"

DETECTOR_THRESHOLD = 60

#RemoteCam
REMOTECAM_PORT = 10000
REMOTECAM_NBSOCKETS = 3
REMOTECAM_LENGTH = 1280
REMOTECAM_WIDTH = 720
REMOTECAM_DIM = 3

DISPLAY_LENGTH = 1280
DISPLAY_WIDTH = 720
DISPLAY_SIZE = 3

SOCKET_BUFSIZE = 65000