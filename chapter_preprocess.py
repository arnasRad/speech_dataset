import os
from utils import replace_utils as ru, split_utils as su
import properties


def process_chapters_in_directory():
    # for filename in os.listdir(properties.book_original_text_dir):
    #     if filename.endswith(".txt"):
    #         print("filename: %s" % filename)
    #         replace_chapter_text(filename)
    for chapter_index in range(1, properties.book_chapter_count+1):
        split_long_chapter(chapter_index)


def replace_chapter_text(filename):
    ru.replace_and_rewrite_file(file_path=os.path.join(properties.book_original_text_dir, filename),
                                pattern=properties.new_line_regex,
                                string_replacement="\n\n")


def split_long_chapter(chapter_index):
    chapter_filename = properties.text_filename % chapter_index

    su.split_long_chapter(chapter_file_path=os.path.join(properties.book_original_text_dir, chapter_filename),
                          output_path=properties.book_preproc_text_dir,
                          chapter_index=chapter_index,
                          length_limit=27000)


process_chapters_in_directory()
