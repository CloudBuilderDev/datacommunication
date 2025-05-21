FREQ_START = 512         # START 기준 주파수
FREQ_STEP = 192          # 주파수 간격 (자유롭게 조정 가능)

HEX_LIST = ['0', '1', '2', '3', '4',
            '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E', 'F']

HEX = set(HEX_LIST)

rules = {}

# START 신호 주파수 설정
rules['START'] = FREQ_START

# 0 ~ F 에 주파수 할당
for i, h in enumerate(HEX_LIST):
    # START보다 1 STEP 띄우고, 이후 1씩 증가 (i+1)
    rules[h] = FREQ_START + FREQ_STEP + FREQ_STEP * (i + 1)

# END 신호 주파수는 마지막보다 2칸 더 띄우기
rules['END'] = FREQ_START + FREQ_STEP + FREQ_STEP * (len(HEX_LIST) + 2)

if __name__ == '__main__':
    print(f"FREQ_START: {FREQ_START}, FREQ_STEP: {FREQ_STEP}")
    print("Frequency Rules:")
    for k in sorted(rules, key=lambda x: (rules[x])):
        print(f"{k}: {rules[k]} Hz")

