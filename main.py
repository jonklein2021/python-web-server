# Jon Klein
# CSE 342 - HW 2

import datetime
from socket import *
import urllib.request

# get public IP
publicip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

# set up TCP server with parameters
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

# store logs here
logs = []

print(f'Server listening on 127.0.0.1:{serverPort} and {publicip}:{serverPort}')

# loop to keep server running
while True:
    # accept new connection
    connectionSocket, addr = serverSocket.accept()
    ip, port = addr
    connectionSocket.settimeout(10)
    print(f'Connection from {ip}:{port}')
    
    # receive message from client or timeout
    try:
        sentence = connectionSocket.recv(1024).decode(errors='ignore')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request = sentence.split('\n')[0].split(' ')
        
        # verify the request is a HTTP GET request
        if request[0] != "GET":
            print("Invalid GET request. Closing connection.")
            connectionSocket.close()
            break # TODO: change this
        
        # determine the requested file; recall that "/" => "index.html"
        requestedFile = "static" + (request[1] if request[1] != "/" else "/index.html")
        
        # append request to logs
        logs.append(f"[{timestamp}] {ip}:{port} requests {requestedFile}\n")
        
        # check if file exists
        try:
            with open(requestedFile, 'rb') as file:
                # send response to client
                response = b"HTTP/1.1 200 OK\n\n" + file.read()
                connectionSocket.send(response)
        except FileNotFoundError:
            # send response to client
            response = "HTTP/1.1 404 Not Found\n\n404 Not Found"
            connectionSocket.send(response.encode())
        
    except timeout:
        print("Client timed out.")
    finally:
        # write logs to log.txt and close connection
        with open("log.txt", "a") as logfile:
            logfile.writelines(logs)
            
        connectionSocket.close()
    
