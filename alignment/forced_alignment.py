from aeneas.executetask import ExecuteTask
from aeneas.task import Task

import properties
from files import file_utils as fu


def force_align(book_name, chapter_index):
    print("Aligning chapter {:d}".format(chapter_index))
    # create Task objects
    task = Task(config_string=properties.aeneas_configuration_string)

    task.audio_file_path_absolute = fu.build_audio_path(book_name, chapter_index)
    task.text_file_path_absolute = fu.build_valid_text_path(book_name, chapter_index)
    task.sync_map_file_path_absolute = fu.build_syncmap_path(book_name, chapter_index)

    # process Task
    ExecuteTask(task).execute()

    # output sync map to file
    task.output_sync_map_file()
