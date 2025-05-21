import math
import statistics
import struct
import time
import wave
import pyaudio
import re
import morse_data
import textToMorse
import morseToText
import decode_morse_from_audio
INTMAX = 2**15 - 1  # 32767
UNIT = 0.1                # 1 unit = 100ms
FREQ = 523.251            # C5 tone
FS = 48000                # 샘플레이트
MORSE_THRESHOLD = 1000    # 임계값 (환경에 따라 조정 필요)
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16

# Morse Code 테이블
MORSE_CODE_DICT = morse_data.MORSE_DICT

def send_data():
    text = input("Enter text to send (A-Z, 0-9 only): ").strip()
    morse = textToMorse.text2morse(text)
    print("Morse:", morse)

    # PyAudio 스트림을 한 번만 열기
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=1,
                    rate=FS,
                    output=True) # 출력 스트림

    def play_tone(units):
        num_samples = int(FS * UNIT * units)
        samples = [
            int(INTMAX * math.sin(2 * math.pi * FREQ * (i / FS))) # 사인파 생성
            for i in range(num_samples)
        ]
        packed = struct.pack('<' + 'h' * len(samples), *samples) # 바이너리로 변환
        stream.write(packed)

    def play_silence(units):
        num_samples = int(FS * UNIT * units)
        silence = [0] * num_samples
        packed = struct.pack('<' + 'h' * len(silence), *silence)
        stream.write(packed)

    # Morse 재생
    for symbol in morse:
        if symbol == '.':
            play_tone(1)       # 1 unit
            play_silence(1)    # 기호 사이
        elif symbol == '-':
            play_tone(3)       # 3 units
            play_silence(1)    # 기호 사이
        elif symbol == ' ':
            play_silence(3)    # 문자 사이
        elif symbol == '/':
            play_silence(7)    # 단어 사이

    stream.stop_stream()
    stream.close()
    p.terminate()

unit_samples = int(FS*UNIT) # 4800 samples

def receive_data():
    print("Recording...")
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=FS, input=True)

    audio = []
    started = False
    unseen_count = 0

    while True:
        raw = stream.read(unit_samples)
        chunk = struct.unpack('<' + 'h' * unit_samples, raw)
        std = statistics.stdev(chunk)

        if not started:
            if std > MORSE_THRESHOLD:
                print("Signal detected! Starting recording...")
                started = True
                audio.extend(chunk)
            else:
                print("Waiting... std =", std)
        else:
            print(f"Recording... std = {std:.3f}")
            audio.extend(chunk)
            if std < MORSE_THRESHOLD:
                unseen_count += 1
            else:
                unseen_count = 0

            if unseen_count >= 30: # 3초간 무음이면 종료
                print("Silence too long. Stopping recording.")
                break

    stream.stop_stream()
    stream.close()
    p.terminate()
    print(f"Recording finished. Total units recorded: {len(audio)//unit_samples}")


    # 분석 및 해독
    morse_str = decode_morse_from_audio.decode_morse_from_audio(audio, FS, UNIT, MORSE_THRESHOLD)
    print("Detected Morse:", morse_str)

    decoded_text = morseToText.morse_to_text(morse_str)
    print("Decoded Text:", decoded_text)

def main():
    while True:
        print('Morse Code over Sound with Noise')
        print('2024 Spring Data Communication at CNU')
        print('[1] Send morse code over sound (play)')
        print('[2] Receive morse code over sound (record)')
        print('[q] Exit')
        select = input('Select menu: ').strip().upper()
        if select == '1':
            send_data()
        elif select == '2':
            receive_data()
        elif select == 'Q':
            print('Terminating...')
            break

if __name__ == '__main__':
    main()







