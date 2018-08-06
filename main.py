# -*- coding: utf-8 -*-

# Projeto Kurupira - Arthur Lorencini Bergamaschi e Ruyhter Maximo

# Bibliotecas

import time
from time import strftime
from time import sleep

# Direcionando a pasta de importação

import sys
sys.path.insert(0, '/home/pi/Desktop/Kurupira/modules')

import os
import RPi.GPIO as GPIO

# Módulos criados 
import camera
import sdirectory as sdir
import dht11
import mfile



# Setup-------------------------------------------

# Testes iniciais
print ("Início de programa...")
mfile.on_log()
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
cte_on = 300 # tempo on sem detectar (em segundos)
sizeLimit = 500 # em MB (ou Mb, não lembro)
sensor_time = 4.7 # tempo (s) do sensor pir. Pode-se alterar o sensor para diminuir o tempo de "debounce"
dht_time = 120 # tempo (s) entre uma leitura e outra do dht11
size_log_time = 30
last_dht = time.time()
last_size = time.time()

GPIO.setup(pir_pin, GPIO.IN)  # Pino de entrada para ler a saída do sensor PIR
GPIO.setup(not_pin, GPIO.IN)   # Este Pino é o pino que ficará conectado a "Not" do Sensor PIR
GPIO.setup(led_test_pin, GPIO.OUT) # Pino de saída para um led de test


GPIO.setup(led2_test_pin, GPIO.OUT) # Para ver se o código ainda está rodando
GPIO.output(led2_test_pin,1)        # Poderia colocar piscando sem parar para ver se está ligado ainda

# Chamando a função do sensor dht11
dht11.sensor_dht_once()
mfile.dht11_log()

# Primeiras fotos e vídeo

if b < sizeLimit: # Verifica se há espaço
    camera.fotos()
else:
    print("Lotado")
#camera.video()


# Loop-------------------------------------------


while(1):
    # Atualiza o tamanho atual da pasta multi
    b = int(sdir.get_size())
    
    if int(time.time()- last_dht) > dht_time:
        print('dhtlog')
        mfile.dht11_log()
        last_dht = time.time()
        
    if int(time.time()- last_size) > size_log_time:
        print('sizelog')
        mfile.size_log(sizeLimit)
        last_size = time.time()
        
    if b > sizeLimit: # Se passou do limite de fotos estipulado
        print('dhtlog')
        mfile.dht11_log()
        
        print('sizelog')
        mfile.size_log(sizeLimit)
        
        sleep(10)
        os.system('/home/pi/Desktop/Kurupira/bash-script/kill_python.sh')

    i = GPIO.input(pir_pin)

    if i == 1: # Movimento detectado
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

        last = time.time() # Atualiza o tempo de detecção

    else: # Caso sem movimento
        print ('Sem movimento')

        if int(time.time()- last) > cte_on: # Se o intervalo sem movimento for maior que "n" segs
            mfile.off_log()
            #time.sleep(10)
            os.system("shutdown 0")   # Desliga o RSP
    sleep(0.5) # Para não ler infinitamente rápido