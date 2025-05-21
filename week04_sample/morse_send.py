import math
import re
import struct
import time
import wave

import pyaudio

INTMAX = 2**(16-1)-1
fs = 48000

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

           
def text2morse(text):
    text = text.upper()
    morse = ''

    for t in text:
        if t == ' ':
            morse += '/'
        elif t in english:
            morse += english[t]
        elif t in number:
            morse += number[t]
        morse += ' '
    print(morse)
    return morse

def morse2audio(morse):
    t = 0.1
    f = 523.251
    audio = []
    index = 0
    for m in morse:

        # index += 1
        # progress = (index / len(morse)) * 100
        # print(f"\r{progress:.1f}%", end='', flush=True)
        # print(f"\n\r{morse[:index]}[{m}]{morse[index+1:]}", end='', flush=True)
        # print(f"\n\r{' ' * index} ^", end='', flush=True)
        # print('\033[2A', end='', flush=True)
        # sleep(0.05)

        if m == ' ':
            for i in range(int(t*fs*1)):
                audio.append(int(0))
        elif m == '/':
            for i in range(int(t*fs*1)):
                audio.append(int(0))
        elif m == '.':
            for i in range(int(t*fs*1)):
                audio.append(int(INTMAX*math.sin(2*math.pi*f*(i/fs))))
        elif m == '-':
            for i in range(int(t*fs*3)):
                audio.append(int(INTMAX*math.sin(2*math.pi*f*(i/fs))))

        for i in range(int(t*fs*1)):
            audio.append(int(0))
    return audio


def audio2file(audio, filename):
    with wave.open(filename, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(4)
        w.setframerate(fs)
        for a in audio:
            w.writeframes(struct.pack('<l', a))
    
    print("saved to", filename)


def send():
    while True:
        print('Type some text (only English and Number)')
        text = input('User input: ').strip()
        if re.match(r'[A-Za-z0-9 ]+', text):
            break

    audio = morse2audio(text2morse(text))
    
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=fs,
                    output=True)

    chunk_size = 4096
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i+chunk_size]
        stream.write(struct.pack('<' + ('h'*len(chunk)), *chunk))

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio2file(audio, 'output.wav')

if __name__ == '__main__':
    send_data()  
