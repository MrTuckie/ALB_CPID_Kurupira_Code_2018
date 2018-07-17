# Projeto Kurupira - Arthur Lorencini Bergamaschi e Ruyhter Maximo

# Bibliotecas

import time
from time import strftime
import os
import RPi.GPIO as GPIO
import picamera as pic


# Outro jeito de calcular o tempo (usado no antigo pir2.py)
# from datetime import datetime
# now = time.time()
# later = time.time()
# diference = int(later - now)


# Setup-------------------------------------------


print(time.strftime("%d_%m_%y_%H:%M:%S")) # Apenas teste

last = time.time()  # Atualiza o tempo de detecção pela primeira vez

# Definindo a função dos pinos
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)  # Pino de entrada para ler a saída do sensor PIR
GPIO.setup(5, GPIO.IN)   # Este Pino é o pino que ficará conectado a "Not" do Sensor PIR
GPIO.setup(40, GPIO.OUT)  # Pino de saída para um led de test
GPIO.setup(38, GPIO.OUT)
GPIO.output(38,1) # Para ver se o código ainda está rodando
                  # Poderia colocar piscando sem parar para ver se está ligado ainda


# Funções para testar a câmera --------------------------------------

def fotos():
    import picamera
    import time
    camera = picamera.PiCamera() # Cria um objeto tipo picamera
    try: # Tenta tirar as "n"-fotos com a data e hora
        for x in range(5):
            time.sleep(0.5)
            camera.capture('/home/pi/Desktop/backup/Kurupira/multi/fotos_teste/%s.jpg' % strftime("%d_%m_%y_%H:%M:%S"))
            print("tirando foto #%d" % x)
    finally:
        camera.close()

def video():  # Função para gravar um video de "n"-segundos
    
    import time
    import picamera

    camera = picamera.PiCamera()
    try:
        print("gravando video...")
        camera.start_recording("/home/pi/Desktop/Kurupira/multi/videos_teste/%s.mjpeg" % strftime("%d_%m_%y_%H:%M:%S"))
        camera.wait_recording(5)
        camera.stop_recording()
    finally:
        camera.close()


def piscaled(): # Função para ter um feedback visual de teste
    for x in range(5):
        GPIO.output(40, 1)
        time.sleep(0.1)
        GPIO.output(40, 0)
        time.sleep(0.1)


# Primeira foto (já tira quando o RSP liga)

fotos()


# Loop--------------------------------------------

while True:
    i = GPIO.input(11) # Valor lógico do pino que recebe o valor do sensor PIR
    time.sleep(0.5)

    if i == 0:              # Se o PIR não detecta nada

        print("Sem movimento %d" % i)
        if int(time.time()-last) > 240: # Se o intervalo sem movimento for maior que "n" segs
            time.sleep(1)
            os.system("shutdown 0")   # Desliga o RSP

    elif i == 1:            # Se foi detectado algum movimento

        print("Movimento detectado %d" % i) # Feedback de terminal
        piscaled() # Feedback visual
        GPIO.output(40, 1)  # Led ON
        time.sleep(4.5)  # Tempo pro Led

        i = GPIO.input(11)  # Vê novamente se detectou algum movimento
                            # Com o intuito de ter certeza que está vendo algo
        if i == 1:
            piscaled()      # Pisca o led como feedback visual
            fotos()  # Tira as fotos
            piscaled() # Pisca novamente
            video()   # Grava um vídeo

        GPIO.output(40, 0)  # Led OFF


        last = time.time() # Atualiza o tempo da detecção