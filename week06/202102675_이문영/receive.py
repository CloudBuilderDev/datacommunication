import pyaudio, struct, numpy as np, scipy.fftpack
from rules import rules

INTMAX = 2**15 - 1
UNIT = 0.1
FS = 48000
CHUNK = int(FS * UNIT)
PADDING = 10
DATA_THRESHOLD = 30 

def receive_data():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=FS, input=True)
    print("Listening...")

    hex_data = ''
    started = False
    end_count = 0

    while True:
        raw = stream.read(CHUNK)
        chunk = struct.unpack('<' + 'h'*CHUNK, raw)

        fft = np.fft.fft(chunk)
        freqs = np.fft.fftfreq(len(chunk), d=1/FS)
        freq = abs(freqs[np.argmax(abs(fft))])
        volume = np.std(chunk)

        if volume < DATA_THRESHOLD:
            print(f"[NOISE] Volume too low ({volume:.2f}) → Ignored")
            continue

        matched = None
        for k, v in rules.items():
            if v - PADDING < freq < v + PADDING:
                matched = k
                break

        if matched == 'START':
            print(f"[START] {matched} with {freq:.1f} Hz")
            started = True
            hex_data = ''
        elif matched == 'END' and started:
            print(f"[END] END with {freq:.1f} Hz")
            end_count += 1
            if end_count >= 2:
                break
        elif matched and matched not in ['START', 'END'] and started:
            hex_data += matched
            print(f"[DATA] {matched} with {freq:.1f} Hz | Current data: {hex_data}")
        else:
            print(f"[FREQ={freq:.1f}] Volume: {volume:.2f}")

    stream.stop_stream(); stream.close(); p.terminate()
    print("raw data :", hex_data)
    print("length:", len(hex_data))

    try:
        decoded = bytes.fromhex(hex_data).decode('utf-8')
    except:
        decoded = '[DECODE ERROR]'
    print("Decoded Text:", decoded)

if __name__ == '__main__':
    receive_data()
