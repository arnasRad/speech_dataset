from pydub import AudioSegment
import pandas as pd
import json
import os
import properties


def chapter_is_split(chapter_index):
    if chapter_index in properties.split_book_chapters:
        return True
    return False


def build_file_paths(chapter_index, sub_index=None):
    if sub_index is None:
        audio_file_path = os.path.join(properties.book_audio_dir, properties.audio_filename % chapter_index)
        syncmap_file_path = os.path.join(properties.book_syncmap_dir, properties.syncmap_filename % chapter_index)
    else:
        audio_file_path = os.path.join(properties.book_audio_dir,
                                       properties.audio_sub_filename % (chapter_index, sub_index))
        syncmap_file_path = os.path.join(properties.book_syncmap_dir,
                                         properties.syncmap_sub_filename % (chapter_index, sub_index))

    return audio_file_path, syncmap_file_path


def build_audio_output_filename(sample_index, chapter_index, sub_index=None):
    if sub_index is None:
        dataset_current_chapter_index = properties.dataset_last_chapter_index + chapter_index
        return properties.dataset_audio_filename % (dataset_current_chapter_index, sample_index)
    else:
        dataset_current_chapter_index = properties.dataset_last_chapter_index + chapter_index
        return properties.dataset_audio_sub_filename % (dataset_current_chapter_index, sub_index, sample_index)


def build_syncmap_sentences(audio_book, syncmap):
    sentences = []
    for fragment in syncmap['fragments']:
        start_time = float(fragment['begin']) * 1000
        end_time = float(fragment['end']) * 1000
        if (end_time - start_time) > 400:
            sentences.append({
                "audio": audio_book[start_time:end_time],
                "text": fragment['lines'][0]
            })
    return sentences


def build_chapter_dataframe(dataframe, sentences, chapter_index, sub_index=None):
    # export audio segment
    for idx, sentence in enumerate(sentences):
        text = sentence['text'].lower()
        filename = build_audio_output_filename(idx, chapter_index, sub_index)
        sentence['audio'].export(os.path.join(properties.dataset_audio_dir, filename), format="wav")
        dataframe = dataframe.append(pd.DataFrame([{
            'filename': filename,
            'text': text,
            'up_votes': 0,
            'down_votes': 0,
            'age': 0,
            'gender': 'male',
            'accent': '',
            'duration': ''
        }], columns=properties.csv_sample_columns))

    return dataframe


def convert_to_training_format(dataframe, chapter_index, sub_index=None):
    audio_path, syncmap_path = build_file_paths(chapter_index, sub_index)

    book = AudioSegment.from_mp3(audio_path)
    with open(syncmap_path) as f:
        syncmap = json.loads(f.read())

    sentences = build_syncmap_sentences(book, syncmap)
    dataframe = build_chapter_dataframe(dataframe, sentences, chapter_index, sub_index)

    return dataframe


def main():
    # make directories if they're not present in project tree
    os.makedirs(properties.dataset_audio_dir, exist_ok=True)

    metadata_path = os.path.join(properties.dataset_dir, properties.metadata_filename)
    if os.path.exists(metadata_path):
        df = pd.read_csv(metadata_path, sep="|", encoding='utf-8')
    else:
        df = pd.DataFrame(columns=properties.csv_sample_columns)

    for chapter_index in range(1, properties.book_chapter_count + 1):
        print("Processing chapter %d..." % chapter_index)
        if not chapter_is_split(chapter_index):
            df = convert_to_training_format(df, chapter_index)
        else:
            df = convert_to_training_format(df, chapter_index, sub_index=1)
            df = convert_to_training_format(df, chapter_index, sub_index=2)

    df.to_csv(os.path.join(properties.dataset_dir, properties.metadata_filename), sep='|', encoding='utf-8', index=False)


main()
