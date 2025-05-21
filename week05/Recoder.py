import math
import statistics     # 표준편차 계산용
import struct         # 오디오 데이터를 바이트 <-> 정수 배열로 변환
import time
import pyaudio        # 오디오 입력/출력 라이브러리

def main():
    t = 10            # 녹음 시간 (초)
    fs = 48000        # 샘플레이트 (1초당 48000 샘플)

    p = pyaudio.PyAudio()  # PyAudio 객체 생성

    # 오디오 입력 스트림 열기 (마이크에서 입력 받음)
    stream = p.open(
        format=pyaudio.paInt32,  # 32bit 정수 PCM 형식
        channels=1,              # Mono (1채널)
        rate=fs,                 # 샘플레이트 48000Hz
        input=True               # 입력 모드
    )

    audio = []         # 전체 녹음 데이터를 저장할 리스트
    chunk_size = 1024  # 한번에 읽을 오디오 데이터 크기 (샘플 단위)

    # 총 몇 번 루프 돌릴지 계산: fs * t / chunk_size 만큼 반복
    for _ in range(0, math.ceil(fs / chunk_size) * t):

        # chunk_size 만큼의 raw byte 데이터를 읽고 → unpack해서 정수 배열로 바꿈
        data = struct.unpack('<' + ('l'*chunk_size), stream.read(chunk_size))

        # 현재 chunk 데이터 전체를 audio에 누적 저장
        audio.extend(data)

        # 이 chunk의 표준편차 출력 (정적 노이즈 측정용으로 사용 가능)
        print(statistics.stdev(data))

    # 스트림 정리
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    main()
