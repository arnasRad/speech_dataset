import json
import os

import properties


def build_book_dir(book_name):
    return os.path.join("books", book_name)


def build_text_dir(book_name):
    return os.path.join(build_book_dir(book_name), "text")


def build_valid_text_dir(book_name):
    return os.path.join(build_book_dir(book_name), "text", "valid")


def build_audio_dir(book_name):
    return os.path.join(build_book_dir(book_name), "audio")


def build_syncmap_dir(book_name):
    return os.path.join(build_book_dir(book_name), "aeneas_syncmap")


def build_audio_path(book_name, chapter_index):
    return os.path.join(build_audio_dir(book_name), properties.audio_filename.format(chapter_index))


def build_text_path(book_name, chapter_index):
    return os.path.join(build_text_dir(book_name), properties.text_filename.format(chapter_index))


def build_valid_text_path(book_name, chapter_index):
    return os.path.join(build_valid_text_dir(book_name), properties.text_filename.format(chapter_index))


def build_syncmap_path(book_name, chapter_index):
    return os.path.join(build_syncmap_dir(book_name), properties.syncmap_filename.format(chapter_index))


def build_dataset_dir():
    return os.path.join("dataset")


def build_dataset_audio_dir():
    return os.path.join(build_dataset_dir(), "audio")


def build_dataset_metadata_path():
    return os.path.join(build_dataset_dir(), properties.metadata_filename)


def build_dataset_audio_path(dataset_chapter_index, sample_index):
    return os.path.join(build_dataset_audio_dir(), build_dataset_audio_filename(dataset_chapter_index, sample_index))


def build_dataset_audio_filename(dataset_chapter_index, sample_index):
    return properties.dataset_audio_filename.format(dataset_chapter_index, sample_index)


def read_file(book_name, chapter_index):
    file_path = build_text_path(book_name, chapter_index)
    with open(file_path, 'r', encoding='utf-8') as fr:
        return fr.read()


def load_syncmap(book_name, chapter_index):
    with open(build_syncmap_path(book_name, chapter_index)) as f:
        return json.loads(f.read())


def write_valid_txt_output(book_name, chapter_index, text):
    file_path = build_valid_text_path(book_name, chapter_index)
    with open(file_path, "w", encoding="utf-8") as fw:
        fw.write(text)