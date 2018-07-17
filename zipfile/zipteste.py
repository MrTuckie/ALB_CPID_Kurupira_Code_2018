import zipfile

for filename in [ 'README.txt', 'example.zip', 
                  'bad_example.zip', 'notthere.zip' ]:
    print ("%20s  %s" % (filename, zipfile.is_zipfile(filename)))
    
zf = zipfile.ZipFile('example.zip', 'r')
print (zf.namelist())