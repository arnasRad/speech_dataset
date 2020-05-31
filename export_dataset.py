import os

import pandas as pd

import properties
from utils import audio_utils as au, file_utils as fu


min_fragment_duration_ms = 400


def __build_syncmap_sentences(chapter_audio, chapter_syncmap):
    sentences = []
    for fragment in chapter_syncmap['fragments']:
        start_time = float(fragment['begin']) * 1000
        end_time = float(fragment['end']) * 1000
        if (end_time - start_time) > min_fragment_duration_ms:
            sentences.append({
                "audio": chapter_audio[start_time:end_time],
                "text": fragment['lines'][0]
            })
    return sentences


def __export_dataset_audio_sample(audio_sample, dataset_chapter_index, syncmap_fragment_index):
    audio_sample.export(
        fu.build_dataset_audio_path(dataset_chapter_index, syncmap_fragment_index),
        format="wav"
    )


def __append_to_metadata(metadata_df, dataset_chapter_index, fragment_index, fragment_text, fragment_audio):
    return metadata_df.append(
            pd.DataFrame(
                [{
                    'filename': fu.build_dataset_audio_filename(dataset_chapter_index, fragment_index),
                    'text': fragment_text,
                    'up_votes': 0,
                    'down_votes': 0,
                    'age': 0,
                    'gender': 'male',
                    'accent': '',
                    'duration': fragment_audio.duration_seconds
                }],
                columns=properties.csv_sample_columns
            )
        )


def __build_chapter_dataframe(dataframe, sentences, dataset_chapter_index):
    for syncmap_fragment_index, sentence in enumerate(sentences):
        trimmed_audio = au.trim_silence(sentence['audio'])
        __export_dataset_audio_sample(trimmed_audio, dataset_chapter_index, syncmap_fragment_index)
        dataframe = __append_to_metadata(dataframe,
                                         dataset_chapter_index,
                                         syncmap_fragment_index,
                                         sentence['text'],
                                         trimmed_audio)

    return dataframe


def __build_metadata_and_export_audio_samples(dataframe, book_name, book_chapter_index, dataset_chapter_index):
    chapter_audio = au.load_mp3_audio(book_name, book_chapter_index)
    syncmap = fu.load_syncmap(book_name, book_chapter_index)

    sentences = __build_syncmap_sentences(chapter_audio, syncmap)
    dataframe = __build_chapter_dataframe(dataframe, sentences, dataset_chapter_index)

    return dataframe


def __export_metadata(dataframe):
    dataframe.to_csv(fu.build_dataset_metadata_path(),
                     sep='|', encoding='utf-8', index=False
                     )


def main():
    os.makedirs(fu.build_dataset_audio_dir(), exist_ok=True)

    df = pd.DataFrame(columns=properties.csv_sample_columns)

    dataset_chapter_index = 1
    for book in properties.book_list:
        print("Exporting book \'{:s}\'.".format(book))
        for book_chapter_index in range(1, properties.chapter_count_in[book] + 1):
            print("Exporting chapter {:d}...".format(book_chapter_index))
            df = __build_metadata_and_export_audio_samples(df, book, book_chapter_index, dataset_chapter_index)
            dataset_chapter_index += 1

    __export_metadata(df)


main()
