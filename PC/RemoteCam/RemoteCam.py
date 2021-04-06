# -*- coding: utf-8 -*-
"""
@author: Anthony Melin
@date: 5/4/2020
"""


import cv2
import numpy as np
import socket
from Utils import decodeJpeg

###################################################################



###################################################################
class RemoteCam:

    
    ###############################################################
    def __init__(self, int_port, nb_socket, timeout=1):

        self.socket_list = []
        
        for n in range(nb_socket):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(("127.0.0.1", int_port+n))
            sock.settimeout(timeout)
            self.socket_list.append(sock)
        
        self.novideo = np.zeros((480,640))
        cv2.putText(self.novideo,'No video', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        
        self.decode = np.zeros((480,640))
        cv2.putText(self.decode,'Decode error', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)


    ###############################################################
    def getFrame(self):
        
        try:
            
            data = b""
            for sock in self.socket_list:
                d, websocketserver_adress = sock.recvfrom(65000)
                data += d
                if len(d) < 65000: break
                
            try:
                return decodeJpeg(data.decode())
            except:
                return self.decode
            
        except socket.timeout:
            return self.novideo
        

    ###############################################################
    def close(self):
        
        for sock in self.socket_list:
            sock.close()
        


###################################################################
if __name__ == "__main__":
    
    import sys
    
    if len(sys.argv) == 3:
        
        int_port_start = int(sys.argv[1])
        int_port_range = int(sys.argv[2])
    
        cam = RemoteCam(int_port_start, int_port_range)

        while cv2.waitKey(1) != ord('q'):

            frame = cam.getFrame()
            cv2.imshow("", frame)

        cam.close()
        cv2.destroyAllWindows()
