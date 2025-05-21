import math          # 사인파 계산용
import struct        # 데이터를 이진(binary)로 변환
import time          # (현재는 사용되지 않음)
import pyaudio       # 오디오 재생용

# 32bit 정수에서 최댓값 (양수 범위 최대치)
INTMAX = 2**(32-1) - 1

def main():
    t = 10               # 재생 시간 (초)
    fs = 48000           # 샘플레이트: 1초에 48000개 샘플 생성
    f = 261.626          # 주파수 (Hz): C4 음 (도)

    audio = []           # 사운드 데이터를 저장할 리스트

    # 10초 동안의 사인파를 샘플 단위로 생성
    for i in range(int(t * fs)):
        sample = math.sin(2 * math.pi * f * (i / fs))   # 사인파 계산
        audio.append(int(INTMAX * sample))              # 정수 범위로 변환해 저장

    # PyAudio 초기화
    p = pyaudio.PyAudio()

    # 오디오 스트림 생성 (32bit 정수, 모노, 주어진 샘플레이트, 출력 모드)
    stream = p.open(
        format=pyaudio.paInt32,
        channels=1,
        rate=fs,
        output=True
    )

    chunk_size = 1024  # 한 번에 전송할 샘플 개수

    # 생성한 사운드 데이터를 chunk 단위로 나눠 재생
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i+chunk_size]

        # struct.pack: 파이썬 리스트 → 바이트 시퀀스로 변환
        packed = struct.pack('<' + ('l' * len(chunk)), *chunk)
        stream.write(packed)

    # 재생 종료
    stream.stop_stream()
    stream.close()
    p.terminate()

# main 함수 실행
if __name__ == '__main__':
    main()
