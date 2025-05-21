import sys
import math
import wave
import struct
import statistics


# 단일 채널(Single channel) WAV 파일을 생성하여 사인파를 저장하는 역할 수행

INTMAX = 2**(32-1)-1
t = 1.0   # t : sound lenght - 생성할 오디오의 길이를 1초로 설정
fs = 48000  # fs : sampling rate - 1초당 샘플링 횟수를 48000으로 설정
f = 261.626  # f : frequency - 사인파의 주파수를 261.626Hz로 설정, 중음 도(C4)의 주파수
audio = [] # audio 리스트를 생성한 후 for 루프를 사용하여 사인파 데이터를 샘플링하여 정수로 변환한 값을 저장.
for i in range(int(t * fs)): 
    audio.append(int(INTMAX * math.sin(2 * math.pi * f * (i / fs))))

# WAV 파일 기록시 정해야 할 것
# Channel (채널): 1-Mono, 2-Stereo
# Sample Width(Sample Size): 샘플 정밀도(1, 2, 4 Bytes)
# Frame Rate(Sample Rate, Sample Frequency): 초당 샘플 개수


filename = 't.wav'
# wb : write binary 
# with : 파일을 열고, 파일을 닫는 것을 자동으로 처리
# w : wave 객체 생성
with wave.open(filename, 'wb') as w:  
# with wave.open(filename, 'wb') as w: 구문을 사용하여 WAV 파일을 생성
    w.setnchannels(1)  
    w.setsampwidth(4)
    w.setframerate(48000)
    for a in audio:
        w.writeframes(struct.pack('<l', a))