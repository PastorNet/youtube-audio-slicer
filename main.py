import youtube_dl
import ffmpeg


def trim(input_path, output_path, start, end_all, duration):
    input_stream = ffmpeg.input(input_path)
    i = start
    i_i = 0
    while i < end_all:
        aud = (
            input_stream.audio
            .filter_('atrim', start=i, end=i+duration)
            .filter_('asetpts', 'PTS-STARTPTS')
        )
        output = ffmpeg.output(aud, output_path+f'sample{i_i}.wav')
        ffmpeg.run_async(output, pipe_stdout=False, pipe_stderr=False, pipe_stdin=False, overwrite_output=True)
        i += duration
        i_i += 1


def download_clip(url, name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'/samples/{name}.wav',
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


if __name__ == '__main__':
    #link_eu = 'https://www.youtube.com/watch?v=DCS6t6NUAGQ'
    #link_ru = 'https://www.youtube.com/watch?v=8s9073kNXgY'
    #noise_profile = 'https://www.youtube.com/watch?v=waGd08Gc1lE'
    #download_clip(link_eu, 'clean_sample')
    #download_clip(link_ru, 'clean_sample_ru')
    #download_clip(noise_profile, 'noise-profile')

    trim('samples/clean_sample.wav', 'samples/sliced_data/', 10, 610, 10)
    trim('samples/clean_sample_ru.wav', 'samples/sliced_data_ru/', 10, 610, 10)
    trim('samples/noise-profile.wav', 'samples/sliced-noise-data/', 10, 610, 10)
