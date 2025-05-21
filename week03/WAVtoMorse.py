import wave
import struct
import statistics
import math
import csv

def file2morse(filename):
    """WAV 파일을 읽어 모스 부호로 변환 (국제 표준 적용)"""
    with wave.open(filename, 'rb') as w:
        framerate = w.getframerate()  # 샘플링 레이트 (48000Hz)
        frames = w.getnframes()  # 총 프레임 수
        sampwidth = w.getsampwidth()  # 샘플 폭 (바이트 단위)
        audio = []

        print(f"샘플링 레이트: {framerate}Hz, 총 프레임 수: {frames}, 샘플 폭: {sampwidth * 8}비트")

        for _ in range(frames):
            frame = w.readframes(1)

            # 샘플 폭에 따라 데이터 언패킹
            if sampwidth == 4:  # 32비트 PCM (signed)
                audio.append(struct.unpack('<i', frame)[0])  # 32비트 정수
            else:
                raise ValueError(f"지원되지 않는 샘플 폭: {sampwidth * 8}비트")

    # **100ms 단위로 신호 분석**
    unit = int(0.1 * framerate)  # 100ms 단위 길이
    morse = ''
    prev_signal = None
    silence_count = 0
    signal_length = 0

    for i in range(0, len(audio), unit):
        segment = audio[i:i+unit] # unit 단위로 신호 분할
        if not segment:
            continue

        stdev = statistics.stdev(segment)  # 100ms 단위 신호의 표준 편차 계산

        # **신호 감지 및 변환**
        if stdev > 10000:  # 신호 감지
            signal_length += 1  # 신호 지속 시간 증가
            prev_signal = 'signal'
            silence_count = 0
        else:  # 무음 감지
            if prev_signal == 'signal':  # 신호 종료 시점
                if 1 <= signal_length <= 2:  # 점(`.`) 감지 (100ms ~ 299ms)
                    morse += '.'
                elif signal_length >= 3:  # 대시(`-`) 감지 (300ms 이상)
                    morse += '-'
                
                signal_length = 0  # 신호 길이 초기화

            silence_count += 1
            if silence_count >= 7:
                morse += ' / '  # 단어 구분 (7유닛)
            elif silence_count >= 3:
                morse += ' '  # 문자 구분 (3유닛)

            prev_signal = 'silence'

    # **문자 사이 공백을 한 칸으로 변환**
    morse = morse.replace('   ', ' ').strip()

    return morse

# 실행 예시
#wav_filename = "output_202102675_이문영.wav"  # 변환할 WAV 파일 이름
#morse_code = file2morse(wav_filename)
#print(f"Extracted Morse Code: {morse_code}")
