import morse_data

# 모스 부호 딕셔너리 가져오기
english = morse_data.english
number = morse_data.number

# 영어 & 숫자 모스 부호를 하나의 딕셔너리로 합치기 (역변환용)
MORSE_DICT = {**english, **number}

# 기존 딕셔너리를 "모스 부호: 문자" 형태로 변환
REVERSED_MORSE_DICT = {value: key for key, value in MORSE_DICT.items()}

def morse_to_text(morse_code):
    morse_code = morse_code.strip()  # 앞뒤 공백 제거
    words = morse_code.split(' / ')  # `/` 기준으로 단어 분리
    decoded_text = []

    for word in words:
        # 여러 개의 공백을 단일 공백으로 변환 후 문자 분리
        letters = word.strip().split()  # split(' ')과 다름
        decoded_word = ''.join(REVERSED_MORSE_DICT.get(letter, '?') for letter in letters)
        decoded_text.append(decoded_word)

    return ' '.join(decoded_text)  # 단어 간 공백 추가

# 실행 예시 (쉘 입력 오류 방지)
#morse_input = input("모스 부호를 입력하세요 (단어 간 `/` 사용, 문자 간 공백은 1칸): ").strip()

# 쉘에서 `/` 인식 오류 방지 → 작은따옴표(`'`)나 큰따옴표(`"`)로 입력할 것 권장
#if morse_input.startswith('/'):
    morse_input = morse_input.lstrip('/').strip()  # 앞에 `/`가 오면 제거

#decoded_text = morse_to_text(morse_input)
#print(f"해석된 텍스트: {decoded_text}")
