import morse_data

# 모스 부호 딕셔너리 가져오기

REVERSED_MORSE_DICT = morse_data.REVERSE_MORSE_DICT


def morse_to_text(morse_code):
    morse_code = morse_code.strip()  # 앞뒤 공백 제거
    morse_code.upper()  # 모든 문자를 대문자로 변환
    words = morse_code.split(' / ')  # `/` 기준으로 단어 분리
    decoded_text = []

    for word in words:
        # 여러 개의 공백을 단일 공백으로 변환 후 문자 분리
        letters = word.strip().split()  # split(' ')과 다름
        decoded_word = ''.join(REVERSED_MORSE_DICT.get(letter, '?') for letter in letters)
        decoded_text.append(decoded_word)

    return ' '.join(decoded_text)  # 단어 간 공백 추가

if __name__ == '__main__':
    print("Morse to Text Decoder Test")
    morse_input = input("Enter Morse code (use / between words): ").strip()
    result = morse_to_text(morse_input)
    print("Decoded Text:", result)