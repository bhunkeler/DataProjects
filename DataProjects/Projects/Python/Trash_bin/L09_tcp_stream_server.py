import socket
import time
from datetime import datetime

PORT = 65433
HOST = '192.168.0.151'
# HOST = '127.0.0.1'


# def getMasterNodeIP():
#   from urllib.parse import urlparse
#   try:
#     url_parsed = urlparse(sc.uiWebUrl)
#     ip = url_parsed.netloc.split(':')[0]
#     return ip
#   except Exception as exp:
#     print(exp)
#     return None

print(' ')      
print('TCP Stream Server: {0} - listening on port: {1}'.format(HOST, PORT))      

def send(sensor_data):
  
  ifile  = open(sensor_data, 'r') 
  i = 0
          
  while True:
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # client_socket.bind((getMasterNodeIP(), port))
    client_socket.bind((HOST, PORT))
    client_socket.listen(10)
    conn, addr = client_socket.accept()
    
    try:  
      while True:
        start = time.time()
        ifile  = open(sensor_data, 'r') 
        
        for row in ifile.readlines() :
          
          print("sending: "+ row.rstrip() + "," + str(datetime.now()))

          message = row.rstrip() + ',' + str(datetime.now()) + "\n"
          message = message.encode()
          conn.send(message)
          
          time.sleep(0.2)
                   
    except Exception as e:
        if e.errno == 32:
          # Broken Pipe Exception
          print("Socket was closed. Re-initializing")
        else:
          print(str(e))
        conn.close()
        client_socket.close()
        continue
    finally:
        conn.close()
        client_socket.close()

send("data/streaming/sz/sz_0.json")