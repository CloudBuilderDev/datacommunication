#Create socket
import socket
HOST = '127.0.0.1'
PORT = 65432 
data = ""
# IPv4(AF_INET) and TCP(SOCK_STREAM) socket created
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Bind socket to local host and port
    sock.bind((HOST, PORT))
    #Listen for one connection at a time
    sock.listen(1)

    print("Waiting for connection...")
    #Accept connection
    conn, addr = sock.accept()
    with conn:
        while(True) :
            #Read one by one
            bit = conn.recv(1).decode('utf-8') 
            if not bit:
                break
            print("BIT : " + bit)
            data += bit
        print("Received data : " + data)    

characters = ""
n=8
splitData = [data[i:i+n] for i in range(0, len(data), n)]
print("Data received : " + str(splitData))

i=0

for x in splitData:
    splitString = splitData[i]
    splitInteger = int(splitString,2)
    characters += str(chr(splitInteger))
    i+=1
print("Message Converted: " + characters)