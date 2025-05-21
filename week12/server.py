import socket
import os

FLAGS = _ = None
DEBUG = False
chunksize = 1500  # 기본 전송 단위

# 서버 시작 시 전송 가능한 파일 목록 구성
def build_file_index(directory='.'):
    index = {}  # filename -> (path, size)
    for fname in os.listdir(directory):
        if os.path.isfile(fname):
            index[fname] = (os.path.abspath(fname), os.path.getsize(fname))
            print(f"[DEBUG] Found file: {index[fname][0]} ({index[fname][1]} bytes)")
    return index


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((FLAGS.address, FLAGS.port))
    sock.settimeout(1.0)
    print(f'[INFO] Listening on {FLAGS.address}:{FLAGS.port}')

    file_index = build_file_index()
    print(f'[INFO] File index loaded with {len(file_index)} files')

    while True:
        try:
            data, client = sock.recvfrom(chunksize)
            data = data.decode('utf-8').strip()
            print(f'[INFO] Received: {data} from {client}')

            tokens = data.split(maxsplit=1)
            if len(tokens) != 2:
                sock.sendto(b'400 Bad Request : Invalid request format', client) #byte literal
                continue

            command, filename = tokens
            if filename not in file_index:
                sock.sendto(b'404 Not Found', client)
                print(f'[WARN] {filename} not found')
                continue

            path, size = file_index[filename]

            if command == 'check':
                sock.sendto(str(size).encode('utf-8'), client)
                print(f'[INFO] Sent file size {size} for {filename}')

            elif command == 'download':
                with open(path, 'rb') as f:
                    remain = size
                    while remain > 0:
                        chunk = f.read(chunksize)
                        sock.sendto(chunk, client)
                        remain -= len(chunk)
                        print(f'[INFO] Sent chunk: {len(chunk)} bytes ({remain}B left)')
            else:
                sock.sendto(b'400 Bad Request : Invalid command', client)
        except socket.timeout:
            continue
        except KeyboardInterrupt:
            print(f'[INFO] Shutting down...')
            break
    sock.close()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--address', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=3040)
    FLAGS, _ = parser.parse_known_args()
    main()