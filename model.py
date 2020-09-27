import tensorflow as tf
import librosa as lb
import numpy as np
from cropper import get_np_data, download_clip, trim, download, mixing_data
from plotter import plot_graph
from keras.layers import Input, Dense, Flatten
from keras.models import Model

# option
DOWNLOAD = 0  # download and preprocess the data with little samples (demo)
WAVE_PLOT = 1  # plot original wave, noise wave, mixed wave
DUMP = 0  # dump wave data to real wav
TRAIN_DENOISE = 0  # train the denoising model with mel freq input and output
DENOISE = 0  # use the pretrained denoise autoencoder
PATH = '/root/PycharmProjects/youtube-audio-slicer/samples/'
NPLOAD = 0  # pre-computed data disabled
TRIMMER = 120  # buff of audio


def normalize(noise_data_):
    noise_max = np.max(noise_data)
    expand_rate = 1 / noise_max
    noise_data_ = noise_data * expand_rate
    return noise_data_


if __name__ == '__main__':
    if DOWNLOAD:
        download(10, 600, 60)

    if NPLOAD:
        trim('./samples/clean_sample.wav', './samples/sliced_data/', 10, TRIMMER * 2, TRIMMER)
        trim('./samples/clean_sample_ru.wav', './samples/sliced_data_ru/', 10, TRIMMER * 2, TRIMMER)
        trim('./samples/noise-profile.wav', './samples/sliced-noise-data/', 10, TRIMMER * 2, TRIMMER)
        clean_data, clean_sr = get_np_data(PATH + 'sliced_data_ru/sample0.wav')  # get clear arrays
        noise_data, noise_sr = get_np_data(PATH + 'sliced-noise-data/sample0.wav')  # get noised arrays
        noise_data = normalize(noise_data)
        np.save('npy/clean_data', clean_data)
        np.save('npy/noise_data', noise_data)
        srs = np.append(clean_sr, noise_sr)
        np.save('npy/srs', srs)

    else:
        clean_data = np.load('npy/clean_data.npy')
        noise_data = np.load('npy/noise_data.npy')
        srs = np.load('npy/srs.npy')
        clean_sr = srs.item(0)
        noise_sr = srs.item(1)
        mix_data, mix_sr = mixing_data(clean_sr, noise_sr, clean_data, noise_data)


    if WAVE_PLOT:
        plot_graph(clean_data, noise_data, mix_data, clean_sr, noise_sr, mix_sr)

