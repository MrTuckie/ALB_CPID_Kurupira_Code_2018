import dht11
import time
from time import strftime

def dht11_log():
    file = open('/home/pi/Desktop/Kurupira/logs/dht11_log_temp.txt','a')
    file.write(strftime("%d/%m/%y - %H:%M:%S\n"))
    file.write(str(dht11.sensor_dht_umid_once())+"%")
    file.write('\n')
    file.write(str(dht11.sensor_dht_temp_once())+"ºC")
    file.write('\n\n')

     
    file.close()

def off_log():
    file = open('/home/pi/Desktop/Kurupira/logs/power_log.txt','a')
    file.write(strftime("Desligou: %d/%m/%y - %H:%M:%S\n"))
    file.close()
    
def on_log():
    file = open('/home/pi/Desktop/Kurupira/logs/power_log.txt','a')
    file.write(strftime("Ligou: %d/%m/%y - %H:%M:%S\n"))
    file.close()
