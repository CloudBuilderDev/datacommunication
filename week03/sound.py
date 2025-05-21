########################################################
# 사운드 파일(.wav) 생성 예제 코드
# - 주파수 261.626 Hz의 가운데 도 음을 1초 동안 생성
# - sampling frequency, sample width 값으로 소리 퀄리티 조절
# - palysound 라이브러리를 이용하여 생성된 파일을 재생
########################################################
import sys
import math
import wave
import struct
import statistics

INTMAX = 2**(32-1)-1
t = 1.0    # time duration in seconds
fs = 48000 # sampling frequency (samples per second, Hz)    
f = 261.626 # frequency of the note (C4 pitch in Hz)
audio = []
for i in range(int(t*fs)):
    audio.append(int(INTMAX*math.sin(2*math.pi*f*(i/fs))))

filename = "output.wav"
with wave.open(filename, "w") as wav:
    wav.setnchannels(1) # audio channel(1: mono, 2: stereo)
    wav.setsampwidth(4) # sample width(4 bytes: 32-bit)
    wav.setframerate(fs) # sampling frequency(48000 Hz)
    for s in audio:    # write each sample value of the audio wave to the file
        wav.writeframes(struct.pack("<l", s))

print("saved to", filename)
    
#pip install playsound==1.2.2
from playsound import playsound

playsound(filename)
