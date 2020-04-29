import os
import properties

from aeneas.executetask import ExecuteTask
from aeneas.task import Task


def get_file_paths(chapter_index, sub_index=None):
    if sub_index is None:
        audio_file_path = os.path.join(properties.book_audio_dir, properties.audio_filename % chapter_index)
        text_file_path = os.path.join(properties.book_text_dir, properties.text_filename % chapter_index)
        sync_map_path = os.path.join(properties.book_syncmap_dir, properties.syncmap_filename % chapter_index)
    else:
        audio_file_path = os.path.join(properties.book_audio_dir,
                                       properties.audio_sub_filename % (chapter_index, sub_index))
        text_file_path = os.path.join(properties.book_text_dir,
                                      properties.text_sub_filename % (chapter_index, sub_index))
        sync_map_path = os.path.join(properties.book_syncmap_dir,
                                     properties.syncmap_sub_filename % (chapter_index, sub_index))

    print(audio_file_path + "\n" + text_file_path + "\n" + sync_map_path)

    return audio_file_path, text_file_path, sync_map_path


def force_align(chapter_index, sub_index=None):
    print("aligning chapter %d" % chapter_index)
    # create Task objects
    task = Task(config_string=properties.aeneas_configuration_string)

    task.audio_file_path_absolute, task.text_file_path_absolute, task.sync_map_file_path_absolute = \
        get_file_paths(chapter_index, sub_index)

    # process Task
    ExecuteTask(task).execute()

    # output sync map to file
    task.output_sync_map_file()


def chapter_is_split(chapter_index):
    if chapter_index in properties.split_book_chapters:
        return True
    return False


def main():
    os.makedirs(properties.book_syncmap_dir, exist_ok=True)
    # if processing a lot of chapters, sometimes calculations finish with error (fail) at some chapter;
    # in that case, simply reset the starting chapter index with chapter index that calculations ended
    # with and resume the processing of chapters;
    # if error persists, consider splitting the chapter to reduce it's size and add it to 'split_book_chapters' array
    for chapter in range(1, properties.book_chapter_count + 1):
        if not chapter_is_split(chapter):
            force_align(chapter)
        else:
            force_align(chapter, sub_index=1)
            force_align(chapter, sub_index=2)


main()
