# -*- coding: utf-8 -*-

import picamera
import time
from time import strftime


def fotos():
    "Tira algumas fotos em um determinado tempo"
    camera = picamera.PiCamera() # Cria um objeto tipo picamera
    camera.rotation = 270
    try: # Tenta tirar as "n"-fotos com a data e hora
        for x in range(5):
            time.sleep(0.2)
            camera.capture('/home/pi/Desktop/Kurupira/multi/fotos_teste/%s.jpg' % strftime("%d_%m_%y_%H:%M:%S"))
            print("tirando foto #%d" % (x+1))
    finally:
        camera.close()
        
def video():
    "Função para gravar um video de n-segundos"
    camera = picamera.PiCamera()
    try:
        print("gravando video...")
        camera.start_recording("/home/pi/Desktop/Kurupira/multi/videos_teste/%s.h264" % strftime("%d_%m_%y_%H:%M:%S"))
        # pode trocar o mjpeg por h264
        camera.wait_recording(5)
        camera.stop_recording()
    finally:
        camera.close()

