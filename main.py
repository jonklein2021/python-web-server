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
        parts = sentence.split('\n')
        request = parts[0].split(' ')
        
        # print("Msg:", sentence)
        # print("Parts:", parts)
        # print("Request:", request)
        
        # verify the request is a HTTP GET request
        if request[0] != "GET":
            print("Invalid GET request. Closing connection.")
            connectionSocket.close()
            break # TODO: change this
        
        # determine the requested file; recall that "/" => "index.html"
        requestedFile = request[1] if request[1] != "/" else "index.html"
        # print("Requested file:", requestedFile)
        
        # TODO: check if file exists and send it back if it does
        
        # send response to client
        connectionSocket.send(sentence.encode())
    except timeout:
        print("Client timed out.")
    connectionSocket.close()
