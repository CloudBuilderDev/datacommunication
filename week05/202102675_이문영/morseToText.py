from morse_data import REVERSE_HEX_MORSE_DICT

def morse_to_unicode(morse_code):
    hex_chars = [
        REVERSE_HEX_MORSE_DICT[code]
        for code in morse_code.strip().split()
        if code in REVERSE_HEX_MORSE_DICT
    ]

    hex_str = ''.join(hex_chars)
    if len(hex_str) % 2 != 0:
        return "[DECODE ERROR]"

    try:
        return bytes.fromhex(hex_str).decode('utf-8')
    except:
        return "[DECODE ERROR]"

def check_morse_validity(morse_code_str):
    morse_codes = morse_code_str.strip().split()
    undefined = [code for code in morse_codes if code not in REVERSE_HEX_MORSE_DICT]
    return undefined

if __name__ == '__main__':
    choice = input("Select function: [1] Decode  [2] Check  [q] Quit: ").strip()

    if choice == '1':
        morse_input = input("Enter Morse code: ").strip()
        print("Decoded Text:", morse_to_unicode(morse_input))

    elif choice == '2':
        morse_input = input("Enter Morse code: ").strip()
        undefined = check_morse_validity(morse_input)
        if undefined:
            print("Undefined Morse codes:", ' '.join(undefined))
        else:
            print("All Morse codes are valid.")

    elif choice.lower() == 'q':
        print("Exiting.")
