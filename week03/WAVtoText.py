
from WAVtoMorse import file2morse  # WAV → Morse 변환 코드
from morseToText import morse_to_text  # Morse → Text 변환 코드

def wav_to_text(filename):

    # **Step 1: WAV → Morse 변환**
    morse_code = file2morse(filename)
    print(f"Extracted Morse Code: {morse_code}")

    # **Step 2: Morse → Text 변환**
    decoded_text = morse_to_text(morse_code)
    print(f"Decoded Text: {decoded_text}")

    return decoded_text

wav_filename = "wavs/output_202102675_이문영.wav"  # 변환할 WAV 파일 이름
text_result = wav_to_text(wav_filename)
print(f"최종 변환 결과: {text_result}")
txt_filename = "202102675_이문영.txt"
with open(txt_filename, "w", encoding="utf-8") as txt_file:
    txt_file.write(text_result)

print(f"변환된 텍스트가 파일로 저장되었습니다: {txt_filename}")