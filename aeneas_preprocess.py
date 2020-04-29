import os
import properties
from utils import file_utils as fu, split_utils as su

# load nltk
from nltk import re


def __load_chapter_paragraphs(input_file_path):
    data = fu.read_file(input_file_path)
    return re.split("\n\n", data)


def __join_paragraph_sentences(paragraph_sentence_list):
    text = ""
    for paragraph in paragraph_sentence_list:
        text += "\n".join(paragraph)
        text += "\n"
        # text += "\n\n"
    return text


def preprocess_file(input_file_path, output_file_path):
    print("Processing chapter")
    paragraphs = __load_chapter_paragraphs(input_file_path)
    print("-> paragraphs length: " + str(len(paragraphs)))
    paragraph_sentence_list = su.split_paragraphs_to_sentences(paragraphs)
    print("-> paragraph_sentence_list length: " + str(len(paragraph_sentence_list)))

    book_sentences_text = __join_paragraph_sentences(paragraph_sentence_list)
    valid_book_text = "\n".join(su.split_long_sentences(book_sentences_text))

    with open(output_file_path, "w", encoding="utf-8") as fw:
        fw.write(valid_book_text)
    print('done\n')


def main():
    for filename in os.listdir(properties.book_preproc_text_dir):
        if filename.endswith(".txt"):
            preprocess_file(input_file_path=os.path.join(properties.book_preproc_text_dir, filename),
                            output_file_path=os.path.join(properties.book_text_dir, filename))


main()
