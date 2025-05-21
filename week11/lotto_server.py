
import socket
import random

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((FLAGS.address, FLAGS.port))
    print(f'Listening on {sock}')

    while True:
        data, client = sock.recvfrom(2**16)
        data = data.decode('utf-8').strip()
        print(f'Received {data} from {client}')
        if(data == 'quit') :
            sock.sendto(b'quit this server', client)
            break
        
        user_numbers = set(int(n) for n in data.split())

        lotto_pool = list(set(range(1, 46)) - set(user_numbers))
        needed = 6 - len(user_numbers)
        additional = random.sample(lotto_pool, needed) if needed > 0 else []

        final_numbers = list(user_numbers) + additional
        random.shuffle(final_numbers)
        print(f'Selected Lotto numbers: {final_numbers}')

        response = 'Lotto: ' + ' '.join(map(str, final_numbers))
        print(f'sending client... {response}')
        sock.sendto(response.encode('utf-8'), client)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()


    parser.add_argument('--address', type=str, default='127.0.0.1')

    parser.add_argument('--port', type=int, default=3034)
    
    FLAGS, _ = parser.parse_known_args()
    main()