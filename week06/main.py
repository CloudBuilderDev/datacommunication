from send import send_data
from receive import receive_data

def main():
    while True:
        print("\n[1] Send")
        print("[2] Receive")
        print("[Q] Quit")
        cmd = input("Select: ").strip().upper()
        if cmd == '1': send_data()
        elif cmd == '2': receive_data()
        elif cmd == 'Q': break

if __name__ == '__main__':
    main()
