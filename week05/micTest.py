import pyaudio
import struct
import statistics

CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16-bit (윈도우에서 호환성 좋음)
CHANNELS = 1
RATE = 48000
DEVICE_INDEX = None  # 기본 마이크 사용 (숫자 지정 가능: 5, 9, 11 등)

p = pyaudio.PyAudio()

try:
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=DEVICE_INDEX)

    print("Listening... Speak or make sound (Ctrl+C to stop)")
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        samples = struct.unpack('<' + 'h' * CHUNK, data)
        vol = statistics.stdev(samples)
        bars = '#' * int(vol / 500)
        print(f"{vol:10.2f} | {bars}")
except Exception as e:
    print("Error:", e)
finally:
    try:
        stream.stop_stream()
        stream.close()
    except:
        pass
    p.terminate()
