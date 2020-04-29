import os

# book_chapter_count = 35  # meteoritas
# book_chapter_count = 51  # fenikso_brolija
# book_chapter_count = 25  # hobitas_arba_ten_ir_atgal
# book_chapter_count = 46  # ir_padege_siuos_namus
book_chapter_count = 40

# split_book_chapters = range(1, book_chapter_count)
# split_book_chapters = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20]
# split_book_chapters = [3, 30, 31]  # meteoritas
# split_book_chapters = [3, 4, 6, 7, 12, 14, 16, 17]
# split_book_chapters = [2, 4, 6, 7, 8, 11]
# split_book_chapters = [25, 49, 50, 51]  # fenikso_brolija
# split_book_chapters = [3, 14]  # hobitas_arba_ten_ir_atgal
# split_book_chapters = []  # ir_padege_siuos_namus
split_book_chapters = []

# audio properties
# meteoritas
# audio_split_marks = {
#     3: {"minutes": 18, "seconds": 58.7},
#     30: {"minutes": 16, "seconds": 3.5},
#     31: {"minutes": 15, "seconds": 56.6}
# }
# audio_split_marks = {
#     3: {"minutes": 13, "seconds": 22.4},
#     4: {"minutes": 13, "seconds": 30.3},
#     6: {"minutes": 15, "seconds": 55.2},
#     7: {"minutes": 18, "seconds": 5.1},
#     12: {"minutes": 17, "seconds": 9.8},
#     14: {"minutes": 15, "seconds": 49.5},
#     16: {"minutes": 21, "seconds": 4.7},
#     17: {"minutes": 15, "seconds": 1.9}
# }
# audio_split_marks = {
#     2: {"minutes": 13, "seconds": 31.8},
#     4: {"minutes": 12, "seconds": 30.8},
#     6: {"minutes": 19, "seconds": 0.2},
#     7: {"minutes": 22, "seconds": 2.1},
#     8: {"minutes": 18, "seconds": 9.1},
#     11: {"minutes": 14, "seconds": 44.2}
# }
# fenikso_brolija
# audio_split_marks = {
#     25: {"minutes": 12, "seconds": 46.2},
#     49: {"minutes": 15, "seconds": 41.1},
#     50: {"minutes": 18, "seconds": 17.7},
#     51: {"minutes": 16, "seconds": 8.6}
# }
# hobitas_arba_ten_ir_atgal
# audio_split_marks = {
#     3: {"minutes": 18, "seconds": 10.6},
#     14: {"minutes": 21, "seconds": 15.5}
# }
# ir_padege_siuos_namus
# audio_split_marks = {
# }
#
audio_split_marks = {
}

dataset_last_chapter_index = 157

aeneas_configuration_string = u"task_language=lit|is_text_type=plain|os_task_file_format=json"

# directories
book_dir = os.path.join("books", "vytautas_radzevicius_new", "vakarykstis_pasaulis")
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
