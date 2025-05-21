import wave
import struct
import scipy.fftpack
import numpy as np
from rules import rules  # 주파수 매핑 규칙 필요

unit = 0.1
samplerate = 48000
padding = 5
filename = '실습6-example4-fsk.wav'

print('Raw hex:')
text = ''

with wave.open(filename, 'rb') as w:
    framerate = w.getframerate()
    frames = w.getnframes()
    audio = []

    for i in range(frames):
        frame = w.readframes(1)
        d = struct.unpack('<l', frame)[0]  # 32bit signed int
        audio.append(d)

        # unit(0.1초) 단위로 처리
        if len(audio) >= int(unit * framerate):
            freq = scipy.fftpack.fftfreq(len(audio), d=1 / samplerate)
            fourier = scipy.fftpack.fft(audio)
            top = freq[np.argmax(abs(fourier))]

            data = ''
            for k, v in rules.items():
                if v - padding <= top <= v + padding:
                    data = k
                    break

            if data == 'START':
                print(data)
            elif data == 'END':
                print()
                print(data, end='')
            elif data:
                text += data
                print(data, end='')

            audio.clear()  # 다음 단위로 초기화

print()

try:
    decoded = bytes.fromhex(text).decode("utf-8")
except Exception as e:
    decoded = f"[DECODE ERROR] {e}"

print(f"Decoded: {decoded}")
