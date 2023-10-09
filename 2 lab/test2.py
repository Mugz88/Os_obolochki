import os
import re
import sys 
pid ="26426"
with open("/proc/"+pid+"/mem", 'r') as fp:
    # читаем файл по 20 байт
    chunk = fp.read(20)
    while chunk:
        print(chunk)
        chunk = fp.read(20)