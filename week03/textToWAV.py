from textToMorse import text2morse  # Text → Morse 변환 코드
from MorseToWAV import morse2audio, audio2file  # Morse → WAV 변환 코드

def text_to_wav(text, filename):
    """텍스트를 모스 부호로 변환 후 WAV 파일로 저장"""

    # **Step 1: Text → Morse 변환**
    morse_code = text2morse(text)
    print(f"Converted Morse Code: {morse_code}")

    # **Step 2: Morse → WAV 변환**
    audio_data = morse2audio(morse_code)

    # **Step 3: WAV 파일 저장**
    audio2file(audio_data, filename)
    print(f"WAV 파일이 생성되었습니다: {filename}")

# 실행 예시
if __name__ == "__main__":
    text_input = input("변환할 텍스트를 입력하세요: ").strip()
    wav_filename = "wavs/202102675_이문영.wav"
    text_to_wav(text_input, wav_filename)
    print(f"텍스트를 WAV로 변환 완료: {wav_filename}")
