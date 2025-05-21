from morse_data import HEX_MORSE_DICT

def text2morse_unicode(text):
    # 텍스트를 UTF-8로 인코딩하고 Hex로 변환
    byte_hex = text.encode('utf-8').hex().upper()
    
    # Hex 값을 Morse로 변환
    morse_seq = [HEX_MORSE_DICT[c] for c in byte_hex]  # HEX_MORSE_DICT 사용
    return ' '.join(morse_seq)


if __name__ == "__main__":
    text = input('Enter the text (Unicode): ')

    for ch in text:
        print(f"\n=== Character: '{ch}' ===")
        uni_code = ord(ch)
        print(f"Unicode Integer: {uni_code}")
        binary_code = bin(uni_code)
        print(f"Unicode Binary: {binary_code}")
        code_point = hex(uni_code)
        print(f"Code Point: {code_point}")
        print(f"UTF-8 Bytes: {ch.encode('utf-8')}")
        byte_hex = ch.encode('utf-8').hex().upper()
        print(f"Hex (UTF-8): {byte_hex}")

    # 전체 문자열 기준 인코딩 및 Morse 변환
    total_hex = text.encode('utf-8').hex().upper()
    print(f"\n[ 전체 입력 문자열 ]")
    print(f"UTF-8 Hex: {total_hex}")
    
    morse = text2morse_unicode(text)
    print(f"Morse Code: {morse}")
