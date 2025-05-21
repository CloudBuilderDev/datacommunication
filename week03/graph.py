import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("audio_debug.csv")
plt.plot(df["Index"], df["Amplitude"])
plt.title("WAV 신호 분석")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.show()
