import pyaudio, struct, numpy as np
import reedsolo

INTMAX = 2**15 - 1
UNIT = 0.1
FS = 48000
CHUNK = int(FS * UNIT)
PADDING = 10
DATA_THRESHOLD = 300
DATA_LEN = 12
RSC_LEN = 4
SYMBOL_LEN = DATA_LEN + RSC_LEN


rules = {'START': 512,
'0': 768,
'1': 896,
'2': 1024,
'3': 1152,
'4': 1280,
'5': 1408,
'6': 1536,
'7': 1664,
'8': 1792,
'9': 1920,
'A': 2048,
'B': 2176,
'C': 2304,
'D': 2432,
'E': 2560,
'F': 2688,
'END': 2944}

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
            print(f"[DATA] {matched} with {freq:.1f} Hz \n Current data: {hex_data}")
        else:
            print(f"[FREQ={freq:.1f}] Volume: {volume:.2f}")

    stream.stop_stream(); stream.close(); p.terminate()
    print("raw data(hex string) :", hex_data)
    print("length:", len(hex_data))

    try:
        byte_data = bytes.fromhex(hex_data)
    except:
        byte_data = '[DECODE ERROR]'
    print("byte text:", byte_data)


    rsc = reedsolo.RSCodec(RSC_LEN)
    decoded = ''
    for i in range(0, len(byte_data), SYMBOL_LEN):
        block = byte_data[i:i+SYMBOL_LEN]
        try:
            text_bytes = rsc.decode(block)[0]
            decoded += text_bytes.decode('utf-8')
        except Exception as e:
            print(f"[ERROR] {e} | block: {block}")

    print("복원된 텍스트:", decoded)



if __name__ == '__main__':
    receive_data()
