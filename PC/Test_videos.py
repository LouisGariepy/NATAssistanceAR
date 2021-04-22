from Tensorflow.ObjectDetection import *
from Tensorflow.ObjectDetector import ObjectDetector
from Scenario.Strategy import *


import cv2
import sys
import numpy as np
import unittest

#configuration pour les scenarii
from Scenario.AbstractFactory_Singleton import ContexteFactory2D as conf

Bottle = "Bottle"
Pen = "Pen"
Notebook = "Notebook"
All = [Bottle, Notebook, Pen]

video = {"bottle":'test_videos/bottle.mp4',"pen":'test_videos/pen.mp4',"notebook":'test_videos/notebook.mp4',"all":'test_videos/all.mp4'}

MODEL_DIRECTORY = MODEL_DIRECTORY = os.path.join(os.path.abspath(''),"../ModelsForNAT/model_3")

GRAPH = MODEL_DIRECTORY + "/frozen_inference_graph.pb"
LABELS = MODEL_DIRECTORY + "/labelmap.pbtxt"
NUM_CLASSES = 7

factory = conf.ContexteFactory2D()
scenario = factory.build_strategy().strategy2D

category_index = load_categories(LABELS, NUM_CLASSES)
sess, inputs, outputs = load_model(GRAPH)

detector = ObjectDetector(sess, inputs, outputs, category_index)
detector.SetThreshold(60)
detector.draw = True

class TestObjectDetection(unittest.TestCase):
    # test bottle function
    def test_bottle(self):
        cap = cv2.VideoCapture(video.get("bottle"))
        if (cap.isOpened()== False):
            print("Error opening video  file")

        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                #cv2.imshow('Frame', frame)

                if frame.shape == (720, 1280, 3):
                    # detection
                    detected = detector.Detect(frame)
                    message = "false bottle detection"
                    self.assertEqual(detected.get('classes_names')[0], Bottle, message)
                    scenario.Update(detected, frame)
            cv2.imshow("frame", frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # When everything done, release
        # the video capture object
        cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()

    def test_pen(self):
        cap = cv2.VideoCapture(video.get("pen"))
        if (cap.isOpened()== False):
            print("Error opening video  file")

        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                #cv2.imshow('Frame', frame)

                if frame.shape == (720, 1280, 3):
                    # detection
                    detected = detector.Detect(frame)
                    message = "false pen detection"
                    self.assertEqual(detected.get('classes_names')[0], Pen, message)
                    scenario.Update(detected, frame)
            cv2.imshow("frame", frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # When everything done, release
        # the video capture object
        cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()

    def test_notebook(self):
        cap = cv2.VideoCapture(video.get("notebook"))
        if (cap.isOpened()== False):
            print("Error opening video  file")

        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                #cv2.imshow('Frame', frame)

                if frame.shape == (720, 1280, 3):
                    # detection
                    detected = detector.Detect(frame)
                    message = "false notebook detection"
                    self.assertEqual(detected.get('classes_names')[0], Notebook, message)
                    scenario.Update(detected, frame)
            cv2.imshow("frame", frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # When everything done, release
        # the video capture object
        cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()

    def test_all(self):
        cap = cv2.VideoCapture(video.get("all"))
        if (cap.isOpened()== False):
            print("Error opening video  file")

        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
                #cv2.imshow('Frame', frame)

                if frame.shape == (720, 1280, 3):
                    # detection
                    detected = detector.Detect(frame)
                    message = "false objects detection"
                    list_objects = detected.get('classes_names')
                    list_objects.sort()
                    self.assertEqual(list_objects, All, message)
                    scenario.Update(detected, frame)
            cv2.imshow("frame", frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # When everything done, release
        # the video capture object
        cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()
if __name__ == '__main__':
    unittest.main()