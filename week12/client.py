import socket
FLAGS = _ = None
DEBUG = False
chunksize = 1500 # 1=1byte
def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            filename = input('Filename: ').strip()
            request = f'check {filename}'
            sock.sendto(request.encode('utf-8'), (FLAGS.address, FLAGS.port))

            response, server = sock.recvfrom(chunksize)
            response = response.decode('utf-8')
            if response == '404 Not Found':
                print(response)
                continue
            size = int(response)#UDP - 먼저 파일의 크기를 수신받고 이 크기 만큼 반복문으로 chunksize만큼을 수신한다. 
            request = f'download {filename}'
            sock.sendto(request.encode('utf-8'), (FLAGS.address, FLAGS.port))
            print(f'Request {filename} to ({FLAGS.address}, {FLAGS.port})')

            remain = size
            with open(filename, 'wb') as f:
                while remain > 0:
                    chunk, server = sock.recvfrom(chunksize)
                    f.write(chunk)
                    remain -= len(chunk)
            print(f'File download success')
        except KeyboardInterrupt:
            print(f'Shutting down... {sock}')
            break 
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
    help='The present debug message')

    parser.add_argument('--address', type=str,
    help='The address to send data', default='127.0.0.1')

    parser.add_argument('--port', type=int,
    help='The port to send data', default=3040)

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug
    main()