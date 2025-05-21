
import socket


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f'UDP Lotto Client Ready ({FLAGS.address}:{FLAGS.port})')

    while True:
        data = input("공백을 기준으로 최대 6개까지의 로또 번호를 입력(1~45) \n exit : client exit | quit : server exit \n 입력:").strip()
        if data.lower() == 'exit':
            print("Exiting client.")
            break
        try:
            if data.lower() == 'quit':
                sock.sendto(b'quit', (FLAGS.address, FLAGS.port))
                continue

            nums = [int(n) for n in data.split()]
            if len(nums) > 6:
                print("로또 번호는 최대 6개까지 입력 가능합니다.\n")
                continue
            if not all(1 <= n <= 45 for n in nums):
                print("입력된 번호는 1부터 45 사이여야 합니다.\n")
                continue

        except ValueError:
            print("숫자만 입력해야 합니다.\n")
            continue

        sock.sendto(data.encode('utf-8'), (FLAGS.address, FLAGS.port))
        print(f"Sent: {data}")

        try:
            response, server = sock.recvfrom(2**16)
            print(f"Received: {response.decode('utf-8')}\n")
        except :
            print("서버의 응답을 받는 과정에서 문제 발생\n")
            break
    sock.close()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--address', type=str, default='127.0.0.1', help='Server address')
    parser.add_argument('--port', type=int, default=3034, help='Server port')

    FLAGS, _ = parser.parse_known_args()
    main()
