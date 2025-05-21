import math, struct, pyaudio
from rules import rules

INTMAX = 2**15 - 1
UNIT = 0.1
FS = 48000

def send_data():
    text = input("Enter text to send: ").strip()
    hex_string = text.encode('utf-8').hex().upper()
    print(f"[HEX]: {hex_string}")
    print("length:", len(hex_string))

    audio = []

    def add_wave(freq, units=1):
        samples = [
            int(INTMAX * math.sin(2 * math.pi * freq * i / FS))
            for i in range(int(FS * UNIT * units))
        ]
        audio.extend(samples)

    add_wave(rules['START'], 2)
    for h in hex_string:
        add_wave(rules[h], 1)
    add_wave(rules['END'], 2)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=FS, output=True)
    stream.write(struct.pack('<' + 'h' * len(audio), *audio))
    stream.stop_stream(); stream.close(); p.terminate()
    print("Transmission finished.")

if __name__ == '__main__':
    send_data()