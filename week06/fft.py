import math
import scipy.fftpack
import numpy as np

INTMAX = 2**(32 - 1) - 1
channels = 1
length = 5.0  # 5초간 신호 생성
samplerate = 48000
frequencies = [261.625, 523.251, 1046.502]  # C4, C5, C6
volumes = [1.0, 0.75, 0.5]

waves = []

# 주파수별 사인파 생성
for frequency, volume in zip(frequencies, volumes):
    audio = []
    for i in range(int(length * samplerate)):
        sample = volume * INTMAX * math.sin(2 * math.pi * frequency * i / samplerate)
        audio.append(sample)
    waves.append(audio)

# 여러 파형을 평균하여 track에 합성
track = [0] * int(length * samplerate)
for i in range(len(track)):
    for w in waves:
        track[i] += w[i]
    track[i] /= len(waves)

# 푸리에 변환 수행
freq = scipy.fftpack.fftfreq(len(track), d=1 / samplerate)
fourier = scipy.fftpack.fft(track)

# 주성분 주파수 출력
dominant_freq = freq[np.argmax(abs(fourier))]
print("Dominant frequency:", dominant_freq)

# 세 주파수 근처만 따로 확인 (±0.5Hz 정도 범위)
for i in range(len(freq)):
    if 261.125 <= freq[i] <= 262.125:
        print(f'{i} => {freq[i]}')
    elif 522.751 <= freq[i] <= 523.751:
        print(f'{i} => {freq[i]}')
    elif 1046.002 <= freq[i] <= 1047.002:
        print(f'{i} => {freq[i]}')
