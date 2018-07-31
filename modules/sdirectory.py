import os
def get_size(start_path = '/home/pi/Desktop/Kurupira/multi/'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size/(1024**2)

#print (get_size())
