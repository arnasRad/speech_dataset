book_list = [
    "detektyvas",
    "fenikso_brolija"
]

chapter_count_in = {
    "detektyvas": 37,
    "fenikso_brolija": 51
}

min_dataset_sentence_len = 30  # minimum string length for a sentence in dataset list
max_dataset_sentence_len = 120  # minimum string length for a sentence in dataset list

aeneas_configuration_string = u"task_language=lit|is_text_type=plain|os_task_file_format=json|task_adjust_boundary_algorithm=percent|task_adjust_boundary_percent_value=50"

# filenames
text_filename = "chapter-{:d}.txt"
audio_filename = "audio-{:d}.mp3"
syncmap_filename = "syncmap-{:d}.json"

dataset_audio_filename = "MIF{:04d}-{:04d}.wav"
metadata_filename = "metadata.csv"

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
