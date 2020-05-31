import re

from nltk.tokenize import sent_tokenize

import properties


def __fold_length_of_strings_in_list(string_list):
    length = 0
    for element in string_list:
        length += len(element)
    return length


def __part_length_with_commas(part):
    return len(part) * len(", ")


def __split_sentence_to_valid_length_parts(sentence_parts):
    valid_length_parts = [[]]
    current_part_index = 0
    current_part = valid_length_parts[current_part_index]
    for part in sentence_parts:
        current_optimal_part_length = __fold_length_of_strings_in_list(current_part) + __part_length_with_commas(current_part)
        if (current_optimal_part_length + len(part)) < properties.max_dataset_sentence_len:
            current_part.append(part)
        else:
            current_part_index += 1
            valid_length_parts.append([part])
            current_part = valid_length_parts[current_part_index]
    return valid_length_parts


def split_text_to_paragraphs(text):
    return re.split("\n\n", text)


def split_long_sentences(book_sentences):
    split_sentence_list = []
    for i, sentence in enumerate(book_sentences):
        if len(sentence) > properties.max_dataset_sentence_len:
            sentence_parts = re.split(", |; |[.]{3} | - ", sentence)
            optimal_parts = __split_sentence_to_valid_length_parts(sentence_parts)
            for part in optimal_parts:
                if __fold_length_of_strings_in_list(part) > 0:
                    split_sentence_list.append(", ".join(part))
        else:
            split_sentence_list.append(sentence)
    return split_sentence_list


def split_paragraphs_to_sentences(paragraphs):
    sentences = []
    for paragraph in paragraphs:
        paragraph_sentence_list = sent_tokenize(paragraph)
        sentences += paragraph_sentence_list
    return sentences
