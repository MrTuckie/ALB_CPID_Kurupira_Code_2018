# -*- coding: utf-8 -*-

import picamera
import time
from time import strftime


def fotos():
    camera = picamera.PiCamera() # Cria um objeto tipo picamera
    try: # Tenta tirar as "n"-fotos com a data e hora
        for x in range(4):
            time.sleep(0.3)
            camera.capture('/home/pi/Desktop/Kurupira/multi/fotos_teste/%s.jpg' % strftime("%d_%m_%y_%H:%M:%S"))
            print("tirando foto #%d" % (x+1))
    finally:
        camera.close()
        
def video():  # Função para gravar um video de "n"-segundos
    camera = picamera.PiCamera()
    try:
        print("gravando video...")
        camera.start_recording("/home/pi/Desktop/Kurupira/multi/videos_teste/%s.mjpeg" % strftime("%d_%m_%y_%H:%M:%S"))
        camera.wait_recording(5)
        camera.stop_recording()
    finally:
        camera.close()

