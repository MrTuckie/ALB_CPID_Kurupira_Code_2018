# -*- coding: utf-8 -*-

# Projeto Kurupira - Arthur Lorencini Bergamaschi e Ruyhter Maximo

# Bibliotecas

import time
from time import strftime
from time import sleep

import os
import RPi.GPIO as GPIO

import picamera as pic
import camera
import sdirectory as sdir
#import mfile


# Setup-------------------------------------------

# Testes iniciais
print ("Início de programa...")
a = strftime("%d/%m/%y - %H:%M:%S") # Apenas teste
print (a)
#sdir.get_size()
last = time.time()  # Atualiza o tempo de detecção pela primeira vez
b = int(sdir.get_size())
print ("Espaço da pasta de multimidia: %dMB" % b)

# Definindo a função dos pinos

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Definindo as constantes

pir_pin = 11 # pino do sensor
not_pin = 5  # pino da not com npn
led_test_pin = 40
led2_test_pin = 38
cte_on = 240 # tempo on sem detectar (em segundos)
sizeLimit = 1000 # em MB (ou Mb, não lembro
sensor_time = 4.7 # tempo (s) do sensor pir. Pode-se alterar o sensor para diminuir o tempo de "debounce"


GPIO.setup(pir_pin, GPIO.IN)  # Pino de entrada para ler a saída do sensor PIR
GPIO.setup(not_pin, GPIO.IN)   # Este Pino é o pino que ficará conectado a "Not" do Sensor PIR
GPIO.setup(led_test_pin, GPIO.OUT) # Pino de saída para um led de test


GPIO.setup(led2_test_pin, GPIO.OUT) # Para ver se o código ainda está rodando
GPIO.output(led2_test_pin,1)        # Poderia colocar piscando sem parar para ver se está ligado ainda


# Primeiras fotos e vídeo

if b < sizeLimit: # Verifica se há espaço
    camera.fotos()
else:
    print("Lotado")
#camera.video()


# Loop-------------------------------------------


while(1):
    b = int(sdir.get_size())
    #print b

    if b > sizeLimit: # Se passou do limite de fotos estipulado
        print ('Lotado')
        file = open('/home/pi/Desktop/Kurupira/testfile.txt','w')
        file.write('%d ' % b)
        file.write('em MB (ou mb)\nLimite de espaço para multimídia atingido!')
        file.close()
        os.system('/home/pi/Desktop/Kurupira/bash-script/kill_python.sh')

    i = GPIO.input(pir_pin)
    #j = GPIO.input(not_pin)
    sleep(0.5)

    if i == 1: # Movimento detectado
        #print (j)
        print ('Movimento detectado')
        sleep(sensor_time)
        i = GPIO.input(pir_pin) # Atualiza a leitura do pino na variável
        if i == 1:
            print ('Movimento novamente detectado')
            camera.fotos()
            b = int(sdir.get_size())
            print ("Espaço da pasta de multimidia: %dMB" % b)
            i = GPIO.input(pir_pin)
            if i == 1:
                camera.video()
                b = int(sdir.get_size())
                print ("Espaço da pasta de multimidia: %dMB" % b)
                None

        last = time.time() # Atualiza o tempo de detecção

    else: # Caso sem movimento
        print ('Sem movimento')

        if int(time.time()-last) > cte_on: # Se o intervalo sem movimento for maior que "n" segs
            time.sleep(1)
            os.system("shutdown 0")   # Desliga o RSP
