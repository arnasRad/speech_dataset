import os

out_filename = "chapter-%d.txt"
sub_out_filename = "chapter-%d-%d.txt"


def write_chapter(out_path, chapter_text, chapter_index, chapter_sub_index=None):
    os.makedirs(out_path, exist_ok=True)

    if chapter_sub_index is None:
        with open(os.path.join(out_path, (out_filename % chapter_index)), "w", encoding="utf8") as fw:
            fw.write(chapter_text)
    else:
        with open(os.path.join(out_path, (sub_out_filename % (chapter_index, chapter_sub_index))), "w", encoding="utf8") as fw:
            fw.write(chapter_text)


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as fr:
        return fr.read()


def write_file(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as fw:
        fw.write(text)