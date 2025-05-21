import wave
import math
import numpy as np
import reedsolo
import random

# ---------- [1] 전역 상수 ----------
RSC_LEN = 4
DATA_LEN = 12
SYMBOL_LEN = DATA_LEN + RSC_LEN
UNIT = 0.1
SAMPLERATE = 48000
SHORTMAX = 2**15 - 1
samples_per_unit = int(SAMPLERATE * UNIT)

# 주파수 룰 정의
rules = {
    '0': 1000, '1': 1100, '2': 1200, '3': 1300,
    '4': 1400, '5': 1500, '6': 1600, '7': 1700,
    '8': 1800, '9': 1900, 'A': 2000, 'B': 2100,
    'C': 2200, 'D': 2300, 'E': 2400, 'F': 2500,
    'START': 3000, 'END': 3500,
}
freq2symbol = {v: k for k, v in rules.items()}
HEX = set(rules.keys()) - {'START', 'END'}

# ---------- [2] 사인파 생성 ----------
def generate_tone(freq, duration=UNIT):
    return [SHORTMAX * math.sin(2 * math.pi * freq * i / SAMPLERATE)
            for i in range(int(SAMPLERATE * duration))]

# ---------- [3] 인코딩 + .wav 생성 ----------
def make_wav(text='😊😊😊😊😊', filename='output.wav'):
    byte_hex = text.encode('utf-8')
    rsc = reedsolo.RSCodec(RSC_LEN)
    audio = generate_tone(rules['START'], UNIT*2)

    for k in range(0, len(byte_hex), DATA_LEN):
        block = byte_hex[k:k+DATA_LEN]
        encoded = rsc.encode(block).hex().upper()
        print(f'encoded_data: {encoded}')
        for s in encoded:
            audio += generate_tone(rules[s])

    audio += generate_tone(rules['END'], UNIT*2)
    audio_np = np.array(audio).astype(np.int16)

    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLERATE)
        wf.writeframes(audio_np.tobytes())

    print(f"[+] 저장 완료: {filename}")

# ---------- [4] FFT 피크 탐지 ----------
def fft_peak(chunk):
    windowed = chunk * np.hamming(len(chunk))
    fft_result = np.fft.fft(windowed)
    freqs = np.fft.fftfreq(len(chunk), 1 / SAMPLERATE)
    magnitudes = np.abs(fft_result[:len(chunk)//2])
    peak_idx = np.argmax(magnitudes)
    return abs(freqs[peak_idx])

def nearest_symbol(freq):
    nearest_freq = min(rules.values(), key=lambda x: abs(x - freq))
    return freq2symbol.get(nearest_freq)

# ---------- [5] .wav 디코딩 ----------
def decode_wav(filename='output.wav'):
    with wave.open(filename, 'rb') as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == SAMPLERATE
        raw = wf.readframes(wf.getnframes())

    audio = np.frombuffer(raw, dtype=np.int16)
    symbols = []
    in_payload = False

    for i in range(0, len(audio) - samples_per_unit, samples_per_unit):
        chunk = audio[i:i+samples_per_unit]
        freq = fft_peak(chunk)
        symbol = nearest_symbol(freq)

        if symbol == 'START':
            in_payload = True
            symbols = []
        elif symbol == 'END' and in_payload:
            break
        elif in_payload and symbol in HEX:
            symbols.append(symbol)

    hex_string = ''.join(symbols)
    try:
        byte_data = bytes.fromhex(hex_string)
    except ValueError:
        print("[!] HEX 변환 실패")
        return

    rsc = reedsolo.RSCodec(RSC_LEN)
    decoded = ''
    for i in range(0, len(byte_data), SYMBOL_LEN):
        block = byte_data[i:i+SYMBOL_LEN]
        try:
            text_bytes = rsc.decode(block)[0]
            decoded += text_bytes.decode('utf-8')
        except Exception as e:
            print(f"[!] 복호화 실패 블록: {block.hex()} / {e}")
    print("[*] 복원된 텍스트:", decoded)

# ---------- [6] RS 오류 테스트 ----------
def rs_test(text=' 사용자 입력! '):
    byte_hex = text.encode('utf-8')
    rsc = reedsolo.RSCodec(RSC_LEN)
    encoded = rsc.encode(byte_hex).hex().upper()

    for i in range(RSC_LEN):
        corrupted = list(encoded)
        for r in random.sample(range(len(corrupted)//2), k=i):
            m = random.randint(0, 2)
            if m == 0:
                corrupted[(r-1)*2] = random.choice(list(HEX - {corrupted[(r-1)*2]}))
            elif m == 1:
                corrupted[(r-1)*2+1] = random.choice(list(HEX - {corrupted[(r-1)*2+1]}))
            else:
                corrupted[(r-1)*2] = random.choice(list(HEX - {corrupted[(r-1)*2]}))
                corrupted[(r-1)*2+1] = random.choice(list(HEX - {corrupted[(r-1)*2+1]}))

        corrupted_str = ''.join(corrupted)
        try:
            byte_data = bytes.fromhex(corrupted_str)
            decoded = rsc.decode(byte_data)[0].decode('utf-8')
            if decoded == text:
                print(f"{i}개 오류 복구 성공")
            else:
                print(f"{i}개 오류 복구 실패 (다른 텍스트)")
        except:
            print(f"{i}개 오류 복구 실패")

# ---------- [7] 실행 ----------
if __name__ == '__main__':
    msg = '😊😊😊😊😊'
    make_wav(msg, 'emoji_encoded.wav')
    decode_wav('emoji_encoded.wav')
    rs_test(' 사용자 입력! ')
