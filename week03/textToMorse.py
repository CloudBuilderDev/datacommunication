import morse_data

english = morse_data.english
number = morse_data.number

def text2morse(text):
    words = text.split()  # 단어 단위로 분리
    morse_words = []

    for word in words:
        morse_chars = []
        for char in word:
            if char in english:
                morse_chars.append(english[char])
            elif char in number:
                morse_chars.append(number[char])
        morse_words.append(' '.join(morse_chars))  # 문자 사이 한 칸 공백 추가
    return ' / '.join(morse_words)  # 단어 사이 한 칸 공백 추가

if __name__ == "__main__":
    text = input('문자열을 입력하세요: ')
    morse = text2morse(text)
    print(f"모스 부호: {morse}")