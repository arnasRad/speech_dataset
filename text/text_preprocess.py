from files import file_utils as fu
from text import replace_utils as ru, split_utils as su
from text.merge_utils import ShortSentencesMerger


def __fix_sentences_length(sentences_list):
    # long sentences in a dataset can cause OOM (out of memory) and other errors while training
    # short sentences are often falsely aligned using alignment, they're disatvantage while training, too
    shorter_sentences_list = su.split_long_sentences(sentences_list)
    return ShortSentencesMerger(shorter_sentences_list).merge_short_sentences()


def __get_chapter_sentence_list(book_name, chapter_index):
    book_text = fu.read_file(book_name, chapter_index)
    paragraphs = su.split_text_to_paragraphs(book_text)
    return su.split_paragraphs_to_sentences(paragraphs)


def __join_sentences_to_valid_book_text(sentence_list):
    valid_length_sentences = __fix_sentences_length(sentence_list)
    valid_sentences = ru.remove_invalid_characters_in(valid_length_sentences)
    return "\n".join(valid_sentences)


def preprocess_chapter_text(book_name, chapter_index):
    print("Preprocessing chapter {:d}".format(chapter_index))

    paragraph_sentence_list = __get_chapter_sentence_list(book_name, chapter_index)
    valid_book_text = __join_sentences_to_valid_book_text(paragraph_sentence_list)

    fu.write_valid_txt_output(book_name, chapter_index, valid_book_text)
