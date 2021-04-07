from RemoteCam.RemoteCam import RemoteCam
import cv2
import unittest

camera = RemoteCam(10000, 3)
class TestgetFrameMethod(unittest.TestCase):
    # test function
    def test_novideo(self):
        while True:

            # frame
            frame = camera.getFrame()
            testValue = camera.novideo.tolist() == frame.tolist()
            message = "frame is not equal to novideo."
            self.assertTrue( testValue, message)
            # display
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) == ord('q'): break
        cv2.destroyAllWindows()
        camera.close()
    
    # Returns True or False. 
    def test(self):        
        cap = cv2.VideoCapture('test_videos/all.mp4')
        
        while(cap.isOpened()):
            ret, frame = cap.read()
            
            testValue = camera.novideo.tolist() != frame.tolist()
            message = "frame is equal to novideo."
            self.assertTrue( testValue, message)
            # display
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) == ord('q'): break
        cv2.destroyAllWindows()
        cap.release()

if __name__ == '__main__':
    unittest.main()