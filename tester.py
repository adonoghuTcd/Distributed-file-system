

import os, sys,pdb, errno, socket
from server.server import Server
from utils.helpers import *
from utils.database import Database

import socket
import time

data = 'GET DESKTOP-V5P0GPL:8001 test/ file.py'

def contactserver(data):


    HOST, PORT = socket.gethostname(), 8000
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

     # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data, "utf-8"))

   # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")
    return format(received)


k = contactserver('GET$file.py')
print(k)
time.sleep(1)





