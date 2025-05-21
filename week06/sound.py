import pyaudio
import math
import struct

INTMAX = 2**(32 - 1) - 1  # 32-bit signed int 최대값
channels = 1
length = 5.0  # 5초 동안 재생
samplerate = 48000  # 초당 샘플 수
frequencies = [261.625, 523.251, 1046.502]  # C4, C5, C6
volumes = [1.0, 0.75, 0.5]  # 볼륨 각각 다르게 설정

waves = []

# 주파수별 사인파 생성
for frequency, volume in zip(frequencies, volumes):
    audio = []
    for i in range(int(length * samplerate)):
        sample = volume * INTMAX * math.sin(2 * math.pi * frequency * i / samplerate)
        audio.append(sample)
    waves.append(audio)

# 트랙에 각 파형 합성 (평균값으로 조정)
track = [0] * int(length * samplerate)
for i in range(len(track)):
    for w in waves:
        track[i] += w[i]
    track[i] = round(track[i] / len(waves))

# PyAudio로 재생
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt32, channels=channels, rate=samplerate, output=True)

chunk_size = 1024
for i in range(0, len(track), chunk_size):
    chunk = track[i:i + chunk_size]
    stream.write(struct.pack('<' + 'l' * len(chunk), *chunk))

stream.stop_stream()
stream.close()
p.terminate()
