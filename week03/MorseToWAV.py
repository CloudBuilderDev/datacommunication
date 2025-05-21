import wave
import struct
import math

# 기본 설정
INTMAX = 2**(32-1)-1  # 32-bit PCM 최대값 (2147483647)
UNIT_TIME = 0.1  # 모스 부호의 기본 단위 (100ms)
FS = 48000  # 샘플링 레이트 (48kHz)
FREQ = 523.251  # 기본 주파수 (C5)

def morse2audio(morse):
    """모스 부호를 오디오 샘플 데이터로 변환 (국제 표준 적용)"""
    audio = []

    for symbol in morse:
        if symbol == '.':  # dit (점) - 1유닛
            audio.extend(generate_tone(UNIT_TIME * 1))
        elif symbol == '-':  # dah (대시) - 3유닛
            audio.extend(generate_tone(UNIT_TIME * 3))
        elif symbol == ' ':  # 문자 간 공백 - 3유닛
            audio.extend(generate_silence(UNIT_TIME * 3))
        elif symbol == '/':  # 단어 간 공백 - 7유닛
            audio.extend(generate_silence(UNIT_TIME * 7))

        # 점과 대시 사이 간격 (1유닛 공백 추가)
        audio.extend(generate_silence(UNIT_TIME * 1))

    return audio

def generate_tone(duration):
    """ 특정 주파수(FREQ)의 사인파를 duration(초) 동안 생성 """
    samples = int(FS * duration)
    return [int(INTMAX * math.sin(2 * math.pi * FREQ * (i / FS))) for i in range(samples)]

def generate_silence(duration):
    """ duration(초) 동안 무음(0) 추가 """
    samples = int(FS * duration)
    return [0] * samples

def audio2file(audio, filename):
    """ 오디오 데이터를 32비트 PCM WAV 파일로 저장 """
    with wave.open(filename, 'wb') as w:
        w.setnchannels(1)  # 모노 채널
        w.setsampwidth(4)  # 32-bit PCM (4바이트)
        w.setframerate(FS)  # 샘플링 레이트 48kHz

        for a in audio:
            w.writeframes(struct.pack('<l', a))  # 32-bit 정수 저장

# 실행 예시
#morse_code = input("모스 부호를 입력하세요: ")  
#audio_data = morse2audio(morse_code)
#audio2file(audio_data, "morse_output.wav")

#print("morse_output.wav 파일이 생성되었습니다!")
