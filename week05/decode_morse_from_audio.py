import statistics

def interpret_sequence(bit, count):
    if bit == 1:  # tone
        if count <= 2:
            return '.'  # dit
        elif count <= 5:
            return '-'  # dah
    elif bit == 0:  # silence
        if count <= 2:
            return ''   # 기호 사이
        elif count <= 5:
            return ' '  # 문자 사이
        elif count >= 6:
            return ' / '  # 단어 사이
    return ''


def bits_to_morse(bits):
    morse = ""
    count = 0
    current = bits[0]

    for bit in bits:
        if bit == current:
            count += 1
        else:
            morse += interpret_sequence(current, count)
            current = bit
            count = 1
    morse += interpret_sequence(current, count)
    return morse



def decode_morse_from_audio(audio, FS, UNIT, MORSE_THRESHOLD):
    units_per_chunk = int(FS * UNIT)  # 4800 samples
    morse_bits = []

    # 0.1초 단위로 나눠서 표준편차 측정
    for i in range(0, len(audio), units_per_chunk):
        chunk = audio[i:i + units_per_chunk]
        if len(chunk) < units_per_chunk:
            break
        stdev = statistics.stdev(chunk)
        if stdev > MORSE_THRESHOLD:
            morse_bits.append(1)
        else:
            morse_bits.append(0)

    return bits_to_morse(morse_bits)