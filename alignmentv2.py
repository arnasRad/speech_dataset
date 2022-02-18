import os
from pathlib import Path

from aeneas.executetask import ExecuteTask
from aeneas.task import Task

import properties


def replace_extension(path: Path, new_extension):
    return path.parent / f"{'.'.join(path.name.split('.')[:-1])}.{new_extension}"


def align(txt_path: Path, wav_path: Path):
    print(f"Aligning {txt_path}")
    # create Task objects
    task = Task(config_string=properties.aeneas_configuration_string)

    task.audio_file_path_absolute = str(wav_path)
    task.text_file_path_absolute = str(txt_path)
    task.sync_map_file_path_absolute = replace_extension(txt_path, 'json')

    # process Task
    ExecuteTask(task).execute()

    # output sync map to file
    task.output_sync_map_file()


if __name__ == "__main__":
    input_dir = "/media/arnas/SSD Disk/inovoice/unzipped/child_voice"
    txt_files = [Path(root) / file
                 for root, dirs, files in os.walk(input_dir)
                 for file in files
                 if file.endswith('txt')]
    recording_pairs = {txt: replace_extension(txt, 'wav') for txt in txt_files}

    for txt, wav in recording_pairs.items():
        align(txt, wav)
