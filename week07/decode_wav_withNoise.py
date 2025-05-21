import reedsolo
import random
import math
from rules import rules
import numpy as np
import pyaudio
import math
import wave
import struct
SAMPLERATE = 48000
UNIT = 0.1
DATA_LEN = 12
RSC_LEN = 4
SYMBOL_LEN = DATA_LEN + RSC_LEN
CHUNKSIZE = int(UNIT * SAMPLERATE)


def nearest_symbol(freq):
    freq2symbol = {v: k for k, v in rules.items()}
    nearest = min(rules.values(), key=lambda x: abs(x - freq))
    return freq2symbol.get(nearest)


def fft_peak(chunk):
    fft = np.fft.fft(chunk)
    freqs = np.fft.fftfreq(len(chunk), d=1/SAMPLERATE)
    peak_freq = abs(freqs[np.argmax(np.abs(fft))])
    return peak_freq



def decode_wav(filename):
    with wave.open(filename, 'rb') as w:
        frames = w.readframes(w.getnframes())
    audio = np.frombuffer(frames, dtype=np.int16)
    symbols = []
    started = False
    
    for i in range(0, len(audio) - CHUNKSIZE, CHUNKSIZE):
        chunk = audio[i:i+CHUNKSIZE]
        freq = fft_peak(chunk)
        symbol = nearest_symbol(freq)

        if symbol == 'START':
            started = True
            symbols = []
            continue
        elif symbol == 'END' and started:
            break
        elif started and symbol in '0123456789ABCDEF':
            symbols.append(symbol)

    
    hex_string = ''.join(symbols)
    print("HEX string:", hex_string)
    try:
        byte_data = bytes.fromhex(hex_string)
        print("Byte data:",byte_data)
    except :
        print("HEX 변환 실패")
        return
    
    rsc = reedsolo.RSCodec(RSC_LEN)
    result = ""

    for i in range(0, len(byte_data), SYMBOL_LEN):
        block = byte_data[i:i+SYMBOL_LEN]
        try:
            decoded_bytes = rsc.decode(block)[0]
            result += decoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"복호화 실패: {block.hex()} / {e}")

    print("복원된 텍스트:", result)

    
if __name__ == '__main__':
    decode_wav('output_202102675_이문영_2.wav')