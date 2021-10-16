from socket import *

serverPort = 5253

# This line creates the server’s socket. 
# The first parameter indicates the address family; in particular,AF_INET indicates that 
# the underlying network is using IPv4. The second parameter indicates that the socket is 
# of type SOCK_STREAM, which means it is a TCP socket (rather than a UDP socket, where we use SOCK_DGRAM).
serverSocket = socket(AF_INET, SOCK_STREAM)

# This line binds (that is, assigns) the port number 5253 to the server’s socket. 
# In this manner, when anyone sends a packet to port 5253 at the IP address of the server 
# (localhost in this case), that packet will be directed to this socket.
serverSocket.bind(('localhost', serverPort))

# The serverSocket then goes in the listen state to listen for client connection requests. 
serverSocket.listen(1)

while True:
    print("The server is ready to receive")
    # When a client knocks on this door, the program invokes the accept( ) method for 
    # serverSocket, which creates a new socket in the server, called connectionSocket, 
    # dedicated to this particular client. The client and server then complete the 
    # handshaking, creating a TCP connection between the client’s clientSocket and 
    # the server’s connectionSocket. With the TCP connection established, the client 
    # and server can now send bytes to each other over the connection. With TCP, all
    # bytes sent from one side not are not only guaranteed to arrive at the other 
    # side but also guaranteed to arrive in order
    connectionSocket, addr = serverSocket.accept()
  
    try:
        # wait for data to arrive from the client
        request = connectionSocket.recv(1024)
     
        # identify the request
        requested_file = request.split()[1]
        print('requested file: ', requested_file)

        file_contents = open(requested_file[1:], 'rb')
        send_to_client = file_contents.read()
        print(send_to_client)

        # send it back to client
        connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode('utf-8'))
        if requested_file.decode().endswith('html'):
            connectionSocket.send('Content-Type: text/html\r\n'.encode('utf-8'))
        else:
            connectionSocket.send('Content-Type: image/png\r\n'.encode('utf-8'))
        connectionSocket.send('Accept-Ranges: bytes\r\n\r\n'.encode('utf-8'))
        connectionSocket.send(send_to_client)
        connectionSocket.send('\r\n'.encode('utf-8'))
   
        print('success')

        # close the connectionSocket. Note that the serverSocket is still 
        # alive waiting for new clients to connect, we are only closing the connectionSocket.
        connectionSocket.close()
    except:
        file_error = open('error.html', 'rb')
        send_to_client = file_error.read()

        connectionSocket.send('HTTP/1.1 404 File not found'.encode('utf-8'))
        connectionSocket.send('Content-Type: text/html\r\n'.encode('utf-8'))
        connectionSocket.send('Accept-Ranges: bytes\r\n\r\n'.encode('utf-8'))
        connectionSocket.send(send_to_client)
        connectionSocket.send('\r\n'.encode('utf-8'))

        print('fail')

        connectionSocket.close()
        