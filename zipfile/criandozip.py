from zipfile_infolist import print_info
import zipfile

print ('creating archive')
zf = zipfile.ZipFile('zipfile_write.zip', mode='w')
try:
    print ('adding README.txt')
    zf.write('README.txt')
finally:
    print ('closing')
    zf.close()

print
print_info('zipfile_write.zip')