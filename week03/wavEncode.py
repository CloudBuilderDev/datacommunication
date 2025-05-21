import wave
import morse_data
# 입력된 문자열을 모스 부호로 변환하고,
# 그 모스 부호 기호들(. - /)에 해당하는 .wav 샘플 파일들을 이어붙여,
# 하나의 음성 .wav 파일로 출력하는 프로그램
def morseEncode(message, filename, dump_morse_text=False):
    mc = ''
    message = message.upper()
    for i in message:
        try:
            mc += morse_data.english[i] + ' '  # 2 + 3 units space between letters (1 included)
        except KeyError as e:
            print("Invalid character '" + i + "' skipped.")  # Scream out invalid char

    if(dump_morse_text):  # Dump morse as text
        print(mc)

    wavFiles = []  # Not technically necessary at the moment but leaves the door open
    for l in mc:
        wavFiles.append(l)

    with wave.open(filename+'.wav', 'wb') as output:  # Stitch audio samples and output
        with wave.open("wav-samples/"+wavFiles[0]+".wav") as v:
            output.setparams(v.getparams())
        for infile in wavFiles:
            with wave.open("wav-samples/"+infile+".wav") as s:
                output.writeframes(s.readframes(s.getnframes()))

print("KD9WZZ's Morse to WAV Converter")
while True:
    print("Enter message string (A-Z, 0-9, spaces)")
    userMessage = input(">> ")
    print("Enter output filename (w/o extension):")
    userOutput = input(">> ")
    print("Encoding...")
    morseEncode(userMessage, userOutput)
    print("Done. (CTRL-C to exit)")
