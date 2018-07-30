import dht11

def dht11_log():
    file = open('dht11_log_temp.txt','a') 
 
    file.write(str(dht11.sensor_dht_umid_once()))
    file.write('\n')
    file.write(str(dht11.sensor_dht_temp_once()))
    file.write('\n')

     
    file.close() 
