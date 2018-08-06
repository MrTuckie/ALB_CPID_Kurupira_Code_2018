import dht11
import time
from time import strftime
import sdirectory

def dht11_log():
    file = open('/home/pi/Desktop/Kurupira/multi/logs/dht11_log_temp.txt','a')
    file.write(strftime("%d/%m/%y - %H:%M:%S\n"))
    file.write(str(dht11.sensor_dht_umid_once())+"%")
    file.write('\n')
    file.write(str(dht11.sensor_dht_temp_once())+"ºC")
    file.write('\n\n')     
    file.close()
    
def size_log(max_size):
    b = sdirectory.get_size()
    file = open('/home/pi/Desktop/Kurupira/multi/logs/size_log.txt','a')
    file.write(strftime("%d/%m/%y - %H:%M:%S\n"))
    file.write('%d ' % b)
    file.write('em MB (ou mb)\n')
    if b >= max_size:
        file.write('Lotado\n')
    file.close()


def off_log():
    file = open('/home/pi/Desktop/Kurupira/multi/logs/power_log.txt','a')
    file.write(strftime("Desligou: %d/%m/%y - %H:%M:%S\n"))
    file.close()
    
def on_log():
    file = open('/home/pi/Desktop/Kurupira/multi/logs/power_log.txt','a')
    file.write(strftime("Ligou: %d/%m/%y - %H:%M:%S\n"))
    file.close()
    

