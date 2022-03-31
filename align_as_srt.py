import json
import multiprocessing
import os
import re
from dataclasses import dataclass, replace
from datetime import time
from math import modf
from pathlib import Path
from typing import List

import rx
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from rx import operators as ops
from rx.scheduler import ThreadPoolScheduler

import properties


@dataclass
class SyncmapEntry:
    id: str
    start: str
    end: str
    text: str

    @classmethod
    def from_json_segment(cls, json_segment: dict, idx: int):
        start_time = format_time(json_segment['begin'])
        end_time = format_time(json_segment['end'])
        return cls(
            id=str(idx),
            start=start_time,
            end=end_time,
            text=json_segment['lines'][0]
        )


@dataclass
class Entry:
    txt_filepath: Path = None
    wav_filepath: Path = None
    json_filepath: Path = None
    srt_filepath: Path = None
    text: str = None
    syncmap_entries: List[SyncmapEntry] = None
    srt_data: str = None


def format_time(time_str):
    time_seconds = seconds_str_to_time(time_str)
    return time.strftime(time_seconds, "%H:%M:%S,%f")[:-3]


def seconds_str_to_time(seconds_str):
    milliseconds, seconds = modf(float(seconds_str))
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = seconds // 60
    seconds = seconds % 60
    milliseconds = int(round(milliseconds * 1000))
    return time(hour=hours, minute=minutes, second=seconds, microsecond=milliseconds * 1000)


def read_wdir(directory, recurse) -> List[Entry]:
    if recurse:
        return [Entry(txt_filepath=Path(root) / file)
                for root, dirs, files in os.walk(directory)
                for file in files
                if file.endswith('txt')]
    else:
        return [Entry(txt_filepath=Path(directory) / file)
                for file in os.listdir(directory)
                if file.endswith('txt')]


def set_filepaths(entry: Entry) -> Entry:
    stem = str(entry.txt_filepath.parent / f"{entry.txt_filepath.stem}")
    return replace(entry,
                   wav_filepath=Path(stem + '.wav'),
                   json_filepath=Path(stem + '.json'),
                   srt_filepath=Path(stem + '.srt'),
                   )


def read_txt(entry: Entry) -> Entry:
    with open(entry.txt_filepath, mode='r', encoding='utf-8') as f:
        return replace(entry, text=f.read())


def sentences_to_paragraphs(entry: Entry) -> Entry:
    # assumes all lines are separated with double new lines if at least one double line is found in file
    if not re.search('\n\n', entry.text):
        text = re.sub('\n{2,}', '\n', entry.text)
        entry = replace(entry, text=re.sub('\n', '\n\n', text))

    return entry


def align(entry: Entry):
    print(f"Aligning {entry.txt_filepath}")
    # create Task objects
    task = Task(config_string=properties.aeneas_configuration_string)

    task.audio_file_path_absolute = str(entry.wav_filepath)
    task.text_file_path_absolute = str(entry.txt_filepath)
    task.sync_map_file_path_absolute = str(entry.json_filepath)

    # process Task
    ExecuteTask(task).execute()

    # output sync map to file
    task.output_sync_map_file()


def read_syncmap_entries(entry: Entry) -> Entry:
    with open(entry.json_filepath, mode='r', encoding='utf-8') as syncmap:
        json_data = json.load(syncmap)

    syncmap_entries = [SyncmapEntry.from_json_segment(segment, idx)
                       for idx, segment in enumerate(json_data['fragments'], start=1)]
    return replace(entry, syncmap_entries=syncmap_entries)


def to_srt_data(entry: Entry):
    return replace(entry, srt_data='\n'.join(
        [f"{smap.id}\n{smap.start} --> {smap.end}\n{smap.text}\n" for smap in entry.syncmap_entries]))


def write_srt(entry: Entry):
    with open(entry.srt_filepath, mode='w', encoding='utf-8') as f:
        f.write(entry.srt_data)


if __name__ == "__main__":
    """
    Usage
    - Specify the working directory containing the speech WAV files and TXT files that has corresponding utterances
     (transcriptions)
    - The script aligns all these pairs and outputs both the syncmap JSON and the SRT files
     to the same working directory
    - Specify `recurse_wdir` to also get the WAV and TXT pairs from the child directories of the working directory 
    """
    working_dir = "/home/arnas/Downloads/vaiku-balsai/all/tmp1"
    recurse_wdir = False
    optimal_thread_count = multiprocessing.cpu_count()
    pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

    entries = read_wdir(working_dir, recurse_wdir)
    rx.from_iterable(entries, pool_scheduler).pipe(
        ops.map(set_filepaths),
        ops.map(read_txt),
        ops.map(sentences_to_paragraphs),
        ops.do_action(align),
        ops.map(read_syncmap_entries),
        ops.map(to_srt_data),
        ops.do_action(write_srt),
    ).subscribe(
        on_next=lambda entry: print(f"Converted {entry.srt_filepath}"),
        on_completed=lambda: print("Converting completed"),
        on_error=lambda err: print(f"ERROR: type: {type(err)}, message: {err}"),
    )
