import os
from utils import audio_utils as au
import properties


def split_audios_in_directory(export_without_splitting):
    for i, filename in enumerate(os.listdir(properties.book_long_audio_dir)):
        if filename.endswith(".mp3"):
            print("exporting %s" % filename)
            if (i+1) in properties.split_book_chapters:
                audio = au.load_mp3_audio(os.path.join(properties.book_long_audio_dir, filename))
                first_part, second_part = au.split_audio(i, audio)
                au.export_audio(first_part, i, 1)
                au.export_audio(second_part, i, 2)
            elif export_without_splitting is True:
                audio = au.load_mp3_audio(os.path.join(properties.book_long_audio_dir, filename))
                au.export_audio(audio, i)


split_audios_in_directory(True)
