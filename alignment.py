import os

import properties
from alignment import forced_alignment as fa
from text import text_preprocess as tp
from files import file_utils


def run():
    # If processing a lot of chapters, sometimes calculations finish with error (fail) at some chapter;
    # in that case, simply reset the starting book and chapter index with start_book and start_chapter
    #   that calculations ended with and resume the processing of chapters;
    # If error persists (can't align a single chapter), consider checking if text has accurate transcription of audio
    #   and if it does - split the chapter to smaller chunks.
    # this error is more likely to occur on Windows OS
    start_book = "vakarykstis_pasaulis"
    start_chapter = 38  # chapters range start at index 1

    for current_book in properties.book_list:
        if start_book is not None and start_book != current_book:
            continue
        else:
            start_book = None

        print("Aligning book \'{:s}\'.".format(current_book))
        os.makedirs(file_utils.build_syncmap_dir(current_book), exist_ok=True)
        os.makedirs(file_utils.build_valid_text_dir(current_book), exist_ok=True)

        current_book_chapter_count = properties.chapter_count_in[current_book]
        for chapter_index in range(start_chapter, current_book_chapter_count + 1):
            if chapter_index is current_book_chapter_count:
                start_chapter = 1

            tp.preprocess_chapter_text(current_book, chapter_index)
            fa.force_align(current_book, chapter_index)


if __name__ == "__main__":
    run()
