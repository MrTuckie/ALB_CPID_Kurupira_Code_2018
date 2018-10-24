# -*- coding: utf-8 -*-

# Projeto Kurupira - Arthur Lorencini Bergamaschi.

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

#from gpiozero import Buzzer, InputDevice


# Setup-------------------------------------------

# Testes iniciais ---

print ("Início de programa...")
print (strftime("%d/%m/%y - %H:%M:%S"))


# Indica que horas que ligou no arquivo.
mfile.on_log()

# Atualiza o tempo de detecção pela primeira vez
last = time.time()  

# Recebe o tamanho do armazenamento inicial da pasta multi.
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
rain_pin = 12

sizeLimit = 2000 # em MB (ou Mb, não lembro)

cte_on = 300 # tempo on sem detectar (em segundos)
sensor_time = 4.7 # tempo (s) do sensor pir. Pode-se alterar o sensor para diminuir o tempo de "debounce"
dht_time = 120 # tempo (s) entre uma leitura e outra do dht11
size_log_time = 600 # tempo (s) entre a leitura do espaço da pasta multi
rain_time = 600 # tempo (s) entre as leituras sobre o sensor de chuva

# Ultimas variáveis sendo atualizadas para agora

last_pir = time.time()
last_dht = time.time()
last_size = time.time()
last_rain = time.time()

GPIO.setup(pir_pin, GPIO.IN)  # Pino de entrada para ler a saída do sensor PIR
GPIO.setup(not_pin, GPIO.IN)   # Este Pino é o pino que ficará conectado a "Not" do Sensor PIR
GPIO.setup(led_test_pin, GPIO.OUT) # Pino de saída para um led de test
GPIO.setup(rain_pin,GPIO.IN)

GPIO.setup(led2_test_pin, GPIO.OUT) # Para ver se o código ainda está rodando
GPIO.output(led2_test_pin,1)        # Poderia colocar piscando sem parar para ver se está ligado ainda

# Chamando a função do sensor dht11
dht11.sensor_dht_once()
mfile.dht11_log()
mfile.rain_log(GPIO.input(rain_pin))
mfile.size_log(sizeLimit)

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
    
    # Recebe o valor da entrada do pir
    i = GPIO.input(pir_pin)
    
    # Se o movimento foi detectado
    if i == 1: 
        print ('Movimento detectado')
        sleep(sensor_time) # Tempo para uma leitura e outra
        i = GPIO.input(pir_pin) # Atualiza a leitura do pino na variável
        
        # Se continua detectado depois de sensor_time
        if i == 1:
            print ('Movimento novamente detectado')
            camera.fotos() # Tira fotos
            b = int(sdir.get_size()) # Atualiza o tamanho da pasta multi
            print ("Espaço da pasta de multimidia: %dMB" % b) # Imprime para debugar
            i = GPIO.input(pir_pin) # Atualiza a leitura do pino na variável novamente
            last_pir = time.time() # Atualiza o tempo de detecção
            # Se continua detectado depois disso tudo
            if i == 1:
                camera.video() # Grava vídeo
                b = int(sdir.get_size()) # Atualiza o tamanho da pasta multi
                print ("Espaço da pasta de multimidia: %dMB" % b) # Imprime para debugar

        # last_pir = time.time() # Atualiza o tempo de detecção

    else: # Caso sem movimento
        print ('Sem movimento')
        
        # Se o intervalo sem movimento for maior que "n" segs
        if int(time.time()- last_pir) > cte_on: 
            mfile.off_log() # Diz que desligou
            #time.sleep(10)
            os.system("shutdown 0")   # Desliga o RSP
            sleep(10)    
    
    # Rain Log
    if int(time.time() - last_rain) > rain_time:
        print('rainlog')
        mfile.rain_log(GPIO.input(rain_pin))
        last_rain = time.time()
    
    
    # Dht Log
    if int(time.time()- last_dht) > dht_time:
        print('dhtlog')
        mfile.dht11_log()
        last_dht = time.time()
    
    
    # Size Log
    if int(time.time()- last_size) > size_log_time:
        print('sizelog')
        mfile.size_log(sizeLimit)
        last_size = time.time()
        
        
    # Se passou do limite de fotos estipulado
    if b > sizeLimit: 
        print('dhtlog')
        mfile.dht11_log()
        
        print('sizelog')
        mfile.size_log(sizeLimit)
        
        print('rainlog')
        mfile.rain_log(GPIO.input(rain_pin))
        
        sleep(5)
        # Aqui deve ficar a opção para acionar um pino para desarmar a bateria.
        # Ou algo do tipo
        
        mfile.off_log() # Diz que desligou
        sleep(10)
        os.system("shutdown 0")   # Desliga o RSP
        
        #os.system('/home/pi/Desktop/Kurupira/bash-script/kill_python.sh')
        
        
    sleep(0.5) # Para não ler infinitamente rápido