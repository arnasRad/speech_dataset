from pydub import AudioSegment

from files import file_utils as fu


def load_mp3_audio(book_name, chapter_index):
    return AudioSegment.from_mp3(fu.build_audio_path(book_name, chapter_index))


def _detect_leading_silence(audio, silence_threshold=-50.0, chunk_size=10):
    """
    reference: https://stackoverflow.com/a/29550200
    audio is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    """
    trim_ms = 0  # ms

    assert chunk_size > 0  # to avoid infinite loop
    while audio[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(audio):
        trim_ms += chunk_size

    return trim_ms


def trim_silence(audio):
    start_trim = _detect_leading_silence(audio)
    end_trim = _detect_leading_silence(audio.reverse())

    duration = len(audio)
    return audio[start_trim:duration - end_trim]
