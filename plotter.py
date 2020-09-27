import matplotlib.pyplot as plt
import numpy as np


def plot_graph(clean_data, noise_data, mix_data, clean_sr, noise_sr, mix_sr):
    size = clean_data.shape[0]
    time = np.arange(0, size) * (1.0 / clean_sr)
    plt.figure(1)
    plt.plot(time, clean_data)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("original wavedata")
    plt.grid('on')

    # plot noise wave
    size = noise_data.shape[0]
    time = np.arange(0, size) * (1.0 / noise_sr)
    plt.figure(2)
    plt.plot(time, noise_data)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("noise wavedata")
    plt.grid('on')

    # plot mix wave
    # plot orignial wave
    size = mix_data.shape[0]
    time = np.arange(0, size) * (1.0 / mix_sr)
    plt.figure(3)
    plt.plot(time, mix_data)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("mixed wavedata")
    plt.grid('on')
    plt.show()
