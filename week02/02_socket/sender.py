import time
import socket
HOST = '127.0.0.1'
PORT = 65432 
hasSentComplete = 0

input_string = input("Enter a string: ")
# input string convert to binary string
bit_msg = ''.join([bin(ord(ch))[2:].zfill(8) for ch in input_string])
i = 0

print("Bit string to send: " + str(bit_msg))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    while hasSentComplete == 0:
        time.sleep(.01)
        #print("Loop: {}/{}".format(str(i), str(len(bit_msg))))
        #print("Pogress: {}/100".format(int(i/len(bit_msg)*100)))
        
        # 한 비트씩 전송
        sock.sendall(str(bit_msg[i]).encode()) 
        i += 1

        if i == len(bit_msg):
            hasSentComplete = 1
            print("Data sent: " + str(bit_msg))

