import math
import statistics
import struct
import time

import pyaudio

fs = 48000
chunk_size = 1024

MORSE_THRESHOLD = 700
UNSEEN_THRESHOLD = 3
UNIT = 0.1


english = {'A':'.-'   , 'B':'-...' , 'C':'-.-.' , 'D':'-..'  ,
           'E':'.'    , 'F':'..-.' , 'G':'--.'  , 'H':'....' , 
           'I':'..'   , 'J':'.---' , 'K':'-.-'  , 'L':'.-..' , 
           'M':'--'   , 'N':'-.'   , 'O':'---'  , 'P':'.--.' , 
           'Q':'--.-' , 'R':'.-.'  , 'S':'...'  , 'T':'-'    , 
           'U':'..-'  , 'V':'...-' , 'W':'.--'  , 'X':'-..-' , 
           'Y':'-.--' , 'Z':'--..'  }

number = { '1':'.----', '2':'..---', '3':'...--', '4':'....-',
           '5':'.....', '6':'-....', '7':'--...', '8':'---..', 
           '9':'----.', '0':'-----'}

def morse2text(morse):
    text = ''
    words = morse.split(' '*7)
    for word in words:
        letters = word.split(' '*3)
        for letter in letters:
            letter = letter.replace(' ', '')
            if letter in english.values():
                text += list(english.keys())[list(english.values()).index(letter)]
            elif letter in number.values():
                text += list(number.keys())[list(number.values()).index(letter)]
            else:
                text += letter
        text += ' '
    text = text.strip()
    return text 

def receive():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=fs,
                    input=True)

    audio = []
    morse = ''
    in_signal = False
    start_time = 0
    last_signal_time = time.time()
    empty_time = 0
    sample_per_unit = int(fs * UNIT)  # Calculate chunks needed for 0.1 seconds
    print("Start receiving Morse code...")
    try:
        while True:
            data = struct.unpack('<' + ('h'*chunk_size), stream.read(chunk_size))
            audio.extend(data)
            empty_time = time.time() - last_signal_time

            if statistics.stdev(data) >= MORSE_THRESHOLD:  # 신호 감지
                if not in_signal:
                    start_time = time.time()  # Record signal start time
                    in_signal = True
                    #print("Signal detected!")

            else:  # 신호가 끊어짐
                if in_signal:
                    duration = time.time() - start_time  # 신호 지속 시간 계산
                    empty_time = start_time - last_signal_time
                    #print(f"Empty time: {empty_time:.2f} sec", "start time: ", start_time, "last signal time: ", last_signal_time)
                    #print(f"Signal duration: {duration:.2f} sec")
                    if empty_time < 0.25 and empty_time > 0.05:  # 빈 시간 ( )
                        morse += ' '
                    elif empty_time < 0.65: # 글자 사이
                        morse += '   '
                    elif empty_time < 1: # 단어 사이   
                        morse += '       '
                    if duration < 0.25:  # 짧은 신호 (.)
                        morse += '.'
                    elif duration >= 0.25:  # 긴 신호 (-)
                        morse += '-'

                    last_signal_time = time.time()  # 마지막 신호 시간 업데이트
                    in_signal = False  # 신호 종료
                    print(f"Current morse: {morse}")

            # Check for long silence to end transmission
            if not in_signal and empty_time >= UNSEEN_THRESHOLD:  # 3 seconds of silence
                print('Long silence detected!')
                break

            # Print current Morse code as it's received

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Received Data:", morse2text(morse))

if __name__ == '__main__':
    receive()

