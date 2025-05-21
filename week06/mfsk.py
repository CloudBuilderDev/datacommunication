import math
import struct
import wave
import pyaudio
from rules import rules  # 반드시 rules.py가 있어야 함

INTMAX = 2**(32 - 1) - 1
channels = 1
unit = 0.1
samplerate = 48000

text = ' hello world! 😊'  # 테스트 문자열
string_hex = text.encode('utf-8').hex().upper()
print(f"Text: {text}")
print(f"Hex: {string_hex}")

audio = []

# START 신호 (2unit)
for i in range(int(unit * samplerate * 2)):
    audio.append(int(INTMAX * math.sin(2 * math.pi * rules['START'] * i / samplerate)))

# Hex 문자 → 주파수 → 1unit 사인파
for s in string_hex:
    for i in range(int(unit * samplerate)):
        audio.append(int(INTMAX * math.sin(2 * math.pi * rules[s] * i / samplerate)))

# END 신호 (2unit)
for i in range(int(unit * samplerate * 2)):
    audio.append(int(INTMAX * math.sin(2 * math.pi * rules['END'] * i / samplerate)))

# 사운드 재생
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt32,
                channels=channels,
                rate=samplerate,
                output=True)

chunk_size = 1024
for i in range(0, len(audio), chunk_size):
    chunk = audio[i:i + chunk_size]
    stream.write(struct.pack('<' + 'l' * len(chunk), *chunk))

stream.stop_stream()
stream.close()
p.terminate()

print("Finished playing.")
