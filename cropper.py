import youtube_dl
import ffmpeg
from librosa import load
import numpy as np


def trim(input_path, output_path, start, end_all, duration):
    input_stream = ffmpeg.input(input_path)
    i = start
    i_i = 0
    while i < end_all:
        aud = (
            input_stream.audio
                .filter_('atrim', start=i, end=i + duration)
                .filter_('asetpts', 'PTS-STARTPTS')
        )
        output = ffmpeg.output(aud, output_path + f'sample{i_i}.wav', )
        ffmpeg.run_async(output, pipe_stdout=False, pipe_stderr=False, pipe_stdin=False, overwrite_output=True)
        i += duration
        i_i += 1


def download_clip(url, name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'~/PycharmProjects/youtube-audio-slicer/samples/{name}.wav',
        'noplaylist': True,
        'continue_dl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192', }]
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            ydl.prepare_filename(info_dict)
            ydl.download([url])
            return True
    except Exception:
        return False


def get_np_data(path, count):
    data = np.empty(shape=count)
    temp_data, sr = load(path + 'sample0.wav')
    for x in range(0, count):
        with open(path + f'sample{x}.wav', 'rb') as f:
            np.append(data, np.array(load(path + f'sample{x}.wav', sr=None)))
    return data, sr


def get_np_data(path): #перегрузка
    with open(path, 'rb') as f:
        data, sr = load(path)
    return data, sr


def download(start=10,end=610, buff=60):
    link_eu = 'https://www.youtube.com/watch?v=DCS6t6NUAGQ'
    link_ru = 'https://www.youtube.com/watch?v=8s9073kNXgY'
    noise_profile = 'https://www.youtube.com/watch?v=waGd08Gc1lE'
    download_clip(link_eu, 'clean_sample')
    download_clip(link_ru, 'clean_sample_ru')
    download_clip(noise_profile, 'noise-profile')
    trim('./samples/clean_sample.wav', './samples/sliced_data/', start, end, buff)
    trim('./samples/clean_sample_ru.wav', './samples/sliced_data_ru/', start, end, buff)
    trim('./samples/noise-profile.wav', './samples/sliced-noise-data/', start, end, buff)


def mixing_data(clean_rate, noise_rate, clean_data, noise_data):
    assert clean_rate == noise_rate
    mix_data = clean_data * 0.8 + noise_data * 0.2
    mix_sr = clean_rate
    return mix_data, mix_sr

