import zipfile
import os
import sys
import pyAesCrypt
import hashlib
import io
import zlib
import binascii
import lzma
import lz4.frame
import time

filename = sys.argv[1]
print('FILENAME : ' + filename)

with open("/home/pc-2/testing/{}".format(filename), "rb") as f:
    data = f.read()
    oldHash = hashlib.sha512(data).hexdigest()
    f.close()
    print("OLDHASH: ", oldHash)

with open("/home/pc-2/testing/{}".format(filename), "rb") as f1:
    data = f1.read()
    zipBuffer = io.BytesIO(data)
    zipBuffer.seek(0, io.SEEK_END)
    orgSize = zipBuffer.tell()
#ZLIB
zipBuffer.seek(0)
start = time.process_time()
compressObj = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS)
compress_data = compressObj.compress(zipBuffer.getvalue())
compress_data += compressObj.flush()
print("\nTime taken for ZLIB compression: {}".format(time.process_time() - start))
#LZMA
zipBuffer.seek(0)
startA = time.process_time()
lz_data = lzma.compress(zipBuffer.getvalue())
print("\nTime taken for LZMA compression: {}".format(time.process_time() - startA))
lzObj = io.BytesIO(lz_data)
lzObj.seek(0, io.SEEK_END)
lzSize = lzObj.tell()

#LZ4
zipBuffer.seek(0)
startB = time.process_time()
zdata = lz4.frame.compress(zipBuffer.getvalue())
print("\nTime taken for LZ4 compression: {}".format(time.process_time() - startB))
zObj = io.BytesIO(zdata)
zObj.seek(0, io.SEEK_END)
zSize = zObj.tell()
'''
print(type(compressObj))
print(compressObj)
print(type(compress_data))
print(compress_data)
'''
password = 'foopassword'
bufferSize = 64 * 10242

readInputFileObj = io.BytesIO(compress_data)
readInputFileObj.seek(0, io.SEEK_END)
comSize = readInputFileObj.tell()
print("Org size " + str(orgSize))
print('Zlib Compressed Size ' + str(comSize))
print('LZMA Compressed Size ' + str(lzSize))
print('LZ4 Compressed Size ' + str(zSize))

cipherObj = io.BytesIO()
readInputFileObj.seek(0)
pyAesCrypt.encryptStream(readInputFileObj, cipherObj, password, bufferSize)

print("fileobject  encrypted successfully")

cipherObj.seek(0)
file1 = cipherObj.getvalue()
#print("/n/nCONTENT OF THE FILE : {}".format(file1))
#Calculate size of chunck
split_num = int(len(file1) / 6)
k = 1

#dividing file into chunks
for i in range(0, len(file1), split_num):

    temp_file = open("/home/pc-2/testing/db{}/file.pdf.aes".format(k), "wb")
    if k != 7:
        temp_file.write((file1[i:i + split_num]))
        #chunk = file1[i:i + split_num]
    if k == 7:
        temp_file.write((file1[i:]))
        #chunk = file1[i:]

    print("Document uploaded  to db{}".format(k))
    temp_file.close()
    k += 1

retList = []
for i in range(1, 8):
    with open("/home/pc-2/testing/db{}/file.pdf.aes".format(i), "rb") as f:
        retList.append(f.read())

temp = b"".join(retList)
#print(temp)
fciph = io.BytesIO(temp)
#print(fciph.getvalue())

fdec = io.BytesIO()
ciph_len = len(fciph.getvalue())
fciph.seek(0)
pyAesCrypt.decryptStream(fciph, fdec, password, bufferSize, ciph_len)
print("\n...........DATA DECRYPTED SUCCESASFULLY.......\n")

#print("\n\n{}".format(fdec.getvalue()))

CHUNKSIZE = 1024
fdec.seek(0)
data2 = zlib.decompressobj()
buf = fdec.read(CHUNKSIZE)
#print("buffer data \n", buf)

decompData = data2.decompress(fdec.getvalue())
decompData += data2.flush()

print("Data Decompressed Successfully \n")
with open("/home/pc-2/testing/temp/{}".format(filename), "wb+") as f:
    f.write(decompData)

with open("/home/pc-2/testing/temp/{}".format(filename), "rb") as f:
    data = f.read()
    newHash = hashlib.sha512(data).hexdigest()
    f.close()
    print("OLDHASH: ", newHash)
    if (newHash == oldHash):
        print("\nsame file, Hash matched")
    else:
        print("\nHash did not match")
'''
#Remove aes file if it already exists
if os.path.exists("/home/pc-2/testing/retrievedFile.pdf.aes"):
    os.remove(r"/home/pc-2/testing/retrievedFile.pdf.aes")

#LOCAL
#copy all the files from multiple locations into a single file
for i in range(1, 8):
    with open("/home/pc-2/testing/db{}/file.pdf.aes".format(i), "rb") as f:
        with open("/home/pc-2/testing/retrievedFile.pdf.aes", "ab") as f1:
            for line in f:
                f1.write(line)

print('\nOriginal File Size: ' + str(orgFileSize))
print('\n ZIP File Size: ' + str(zipFileSize))

pyAesCrypt.decryptFile("/home/pc-2/testing/retrievedFile.pdf.aes",
                       "/home/pc-2/testing/{}.zip".format(filename), password,
                       bufferSize)

print("\n FILE DECRYPTED")

with zipfile.ZipFile('{}.zip'.format(filename), 'r') as zipObj:
    zipObj.extractall('/home/pc-2/testing/temp')
print("file unzipped successfully")

with open("/home/pc-2/testing/temp/{}".format(filename), "rb") as f:
    data = f.read()
    newHash = hashlib.sha512(data).hexdigest()
    f.close()
    print("OLDHASH: ", newHash)
    if (newHash == oldHash):
        print("same file, Hash matched")
    else:
        print("Hash did not match")
'''