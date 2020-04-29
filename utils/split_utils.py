import re
from nltk.tokenize import sent_tokenize
from utils import file_utils as fu, replace_utils as ru

max_sentence_length = 120

lithuanian_characters = "ąĄčČęĘėĖįĮšŠųŲūŪžŽ"
french_characters = "ÀàÂâÆæÇçÈèÉéÊêËëÎîÏïÔôŒœÙùÛûÜü"


def __fold_string_list_length(string_list):
    length = 0
    for element in string_list:
        length += len(element)
    return length


def __comma_length(part):
    return len(part) * len(", ")


def __split_sentence_to_valid_length_parts(sentence_parts):
    valid_length_parts = [[]]
    current_part_index = 0
    current_part = valid_length_parts[current_part_index]
    for j, part in enumerate(sentence_parts):
        current_optimal_part_length = __fold_string_list_length(current_part) + __comma_length(current_part)
        if (current_optimal_part_length + len(part)) < max_sentence_length:
            current_part.append(part)
        else:
            current_part_index += 1
            valid_length_parts.append([part])
            current_part = valid_length_parts[current_part_index]
    return valid_length_parts


def split_chapter_in_half(chapter_string):
    chapter_paragraphs = re.split("\n\n", chapter_string)
    half_of_paragraphs_count = len(chapter_paragraphs)//2
    
    first_chapter_half = "\n\n".join(chapter_paragraphs[:half_of_paragraphs_count])
    second_chapter_half = "\n\n".join(chapter_paragraphs[half_of_paragraphs_count:])
    return first_chapter_half, second_chapter_half


def split_book(book_file_path, pattern):
    book_text = fu.read_file(book_file_path)
    return re.split(pattern, book_text)


def split_long_chapter(chapter_file_path, output_path, chapter_index, length_limit):
    chapter = fu.read_file(chapter_file_path)

    chapter_length = len(chapter)
    print("\n\nProcessing chapter %d with length %d" % (chapter_index, chapter_length))
    if chapter_length > length_limit:
        print("splitting chapter %d" % chapter_index)
        chapter_1, chapter_2 = split_chapter_in_half(chapter)
        fu.write_chapter(output_path, chapter_1, chapter_index, 1)
        fu.write_chapter(output_path, chapter_2, chapter_index, 2)
    else:
        print("no need to split chapter %d" % chapter_index)
        fu.write_chapter(output_path, chapter, chapter_index)


def split_long_sentences(book_text):
    sentence_list = re.split("\n", book_text)
    split_sentence_list = []
    for i, sentence in enumerate(sentence_list):
        if len(sentence) > max_sentence_length:
            sentence_parts = re.split(", |; ", sentence)
            # TODO: fix __split_sentence_to_valid_length_parts to not return parts with empty strings
            optimal_parts = __split_sentence_to_valid_length_parts(sentence_parts)
            for part in optimal_parts:
                if __fold_string_list_length(part) > 0:
                    split_sentence_list.append(", ".join(part))
        else:
            split_sentence_list.append(sentence)
    return split_sentence_list


def split_paragraphs_to_sentences(paragraphs):
    paragraph_sentence_list = []
    for paragraph in paragraphs:
        paragraph = ru.replace_aeneas_paragraph(paragraph)
        paragraph_sentence_list.append(sent_tokenize(paragraph))
    return paragraph_sentence_list
