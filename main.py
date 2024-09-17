# Jon Klein
# CSE 342 - HW 2

from socket import *

# set up TCP server with parameters
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('Server listening on port', serverPort)

# loop to keep server running
while True:
    # accept new connection
    connectionSocket, addr = serverSocket.accept()
    ip, port = addr
    connectionSocket.settimeout(10)
    print(f'Connection from {ip}:{port}')
    
    # receive message from client or timeout
    try:
        sentence = connectionSocket.recv(1024).decode()
        request = sentence.split('\n')[0].split(' ')
        
        # verify the request is a HTTP GET request
        if request[0] != "GET":
            print("Invalid GET request. Closing connection.")
            connectionSocket.close()
            break # TODO: change this
        
        # determine the requested file; recall that "/" => "index.html"
        requestedFile = "static/" + (request[1] if request[1] != "/" else "index.html")
        
        # check if file exists
        try:
            with open(requestedFile, 'r') as file:
                # send response to client
                response = "HTTP/1.1 200 OK\n\n" + file.read()
                connectionSocket.send(response.encode())
        except FileNotFoundError:
            # send response to client
            response = "HTTP/1.1 404 Not Found\n\n404 Not Found"
            connectionSocket.send(response.encode())
        
    except timeout:
        print("Client timed out.")
    connectionSocket.close()
