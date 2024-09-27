# Jon Klein
# CSE 342 - HW 2

import datetime
from socket import *
import urllib.request

# get public IP
# source: https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python
publicIP = urllib.request.urlopen('https://ident.me').read().decode('utf8')

# set up TCP server with parameters
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

# write logs here
logFile = "log.txt"

print(f'Server listening on 127.0.0.1:{serverPort} and {publicIP}:{serverPort}')

# loop to keep server running
while True:
    # accept new connection
    connectionSocket, addr = serverSocket.accept()
    ip, port = addr
    connectionSocket.settimeout(10)
    
    # log new connection
    log = f'Connection from {ip}:{port}'
    print(log)
    with open(logFile, "a") as f:
        f.write(log + "\n")
    
    # receive message from client or timeout
    try:
        # need to ignore errors to handle non-ASCII characters in images
        sentence = connectionSocket.recv(1024).decode(errors='ignore')
        
        # source: https://stackoverflow.com/questions/7999935/python-datetime-to-string-without-microsecond-component
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request = sentence.split('\n')[0].split(' ')
        
        # verify the request is a HTTP GET request
        if request[0] != "GET":
            print("Invalid GET request. Closing connection.")
            response = "HTTP/1.1 501 Not Implemented\n\n501 Not Implemented"
            connectionSocket.send(response.encode())
            continue
        
        # determine the requested file; recall that "/" => "index.html"
        requestedFile = "static" + (request[1] if request[1] != "/" else "/index.html")
        
        # append request to logs
        log = f"[{timestamp}] {ip}:{port} requests {requestedFile}"
        print(log)
        with open(logFile, "a") as f:
            f.write(log + "\n")
        
        # check if file exists
        try:
            with open(requestedFile, 'rb') as file:
                # build response and send to client
                response = b"HTTP/1.1 200 OK\n\n" + file.read()
                connectionSocket.send(response)
        except FileNotFoundError:
            # send 404 to client
            response = "HTTP/1.1 404 Not Found\n\n404 Not Found"
            connectionSocket.send(response.encode())
        
    except timeout:
        print("Client timed out.")
    finally:
        # close connection
        connectionSocket.close()    
