from pydub import AudioSegment
import os
import properties


def __minutes_to_seconds(minutes, seconds):
    return minutes * 60 + seconds
    
    
def __split_audio_at_mark(audio, split_mark):
    duration = audio_duration(audio)
    return audio[0:split_mark*1000], audio[split_mark*1000:duration*1000]


def load_wav_audio(audio_path):
    return AudioSegment.from_wav(audio_path)


def load_mp3_audio(audio_path):
    return AudioSegment.from_mp3(audio_path)


def audio_duration(audio):
    frames = audio.frame_count()
    rate = audio.frame_rate
    return frames / rate


def export_audio(audio, index, sub_index=None):
    if sub_index is None:
        audio.export(os.path.join(properties.book_audio_dir, properties.audio_filename % (index+1)), format='mp3')
    else:
        audio.export(os.path.join(properties.book_audio_dir, properties.audio_sub_filename % (index+1, sub_index)), format='mp3')


def split_audio(index, audio):
    audio_split_mark = properties.audio_split_marks[index+1]
    split_mark = __minutes_to_seconds(audio_split_mark['minutes'], audio_split_mark['seconds'])
    return __split_audio_at_mark(audio, split_mark)
