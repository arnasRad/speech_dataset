import os

book_chapter_count = 25

split_book_chapters = [3, 14]  # hobitas_arba_ten_ir_atgal

# hobitas_arba_ten_ir_atgal
audio_split_marks = {
    3: {"minutes": 18, "seconds": 10.6},
    14: {"minutes": 21, "seconds": 15.5}
}

dataset_last_chapter_index = 0

aeneas_configuration_string = u"task_language=lit|is_text_type=plain|os_task_file_format=json"

# directories
book_dir = os.path.join("books", "vytautas_radzevicius_new", "hobitas_arba_ten_ir_atgal")
book_text_dir = os.path.join(book_dir, "text")
book_preproc_text_dir = os.path.join(book_dir, "text", "preproc")
book_original_text_dir = os.path.join(book_dir, "text", "original")
book_audio_dir = os.path.join(book_dir, "audio")
book_long_audio_dir = os.path.join(book_dir, "audio", "long")
book_syncmap_dir = os.path.join(book_dir, "aeneas_syncmap")
dataset_dir = os.path.join("dataset")
dataset_audio_dir = os.path.join(dataset_dir, "audio")

# filenames
text_filename = "chapter-%d.txt"
text_sub_filename = "chapter-%d-%d.txt"
audio_filename = "audio-%d.mp3"
audio_sub_filename = "audio-%d-%d.mp3"
syncmap_filename = "syncmap-%d.json"
syncmap_sub_filename = "syncmap-%d-%d.json"

dataset_audio_filename = "MIF%02d-%04d.wav"
dataset_audio_sub_filename = "MIF%02d-%01d-%04d.wav"
metadata_filename = "metadata.csv"

# patterns
roman_numerals_regex_with_dot = r'\n+[IVX]+\.\s+'
roman_numerals_regex = r'\n+[IVX]+\n+'
new_line_regex = r'\n\n\n'

# metadata properties
csv_sample_columns = [
    'filename',
    'text',
    'up_votes',
    'down_votes',
    'age',
    'gender',
    'accent',
    'duration'
]
