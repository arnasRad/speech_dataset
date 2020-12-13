import argparse
import datetime
import json
import multiprocessing
import os
from dataclasses import dataclass, replace
from datetime import datetime
from datetime import time
from itertools import zip_longest
from math import modf
from pathlib import Path

import rx
from rx import operators as ops
from rx.scheduler import ThreadPoolScheduler


@dataclass()
class Entry:
    basename: str = ''
    dir_path: str = ''
    filepath: Path = None
    out_path: Path = None
    in_data: list = None
    in_fmt: str = ''
    out_data: list = None
    out_fmt: str = ''


def parse_args():
    parser = argparse.ArgumentParser(
        description="Script to convert aeneas syncmaps in input directory to srt (subtitle) format and vice versa. "
                    + "See https://www.speechpad.com/captions/srt",
    )
    parser.add_argument("--input-dir",
                        default="../books/detektyvas/aeneas_syncmap")
    parser.add_argument("--output-dir",
                        default="data/srt")
    parser.add_argument("--to-srt",
                        type=bool,
                        default=True,
                        help="Converts JSON syncmaps in input dir to SRT format. "
                             + "Coverts SRT files to syncmaps otherwise")
    parser.add_argument("--time-fmt",
                        type=str,
                        default="%H:%M:%S,%f",
                        help="SRT file time format")
    return parser.parse_args()


def time_to_seconds(time_str):
    ptime = datetime.strptime(time_str, args.time_fmt)
    hours = ptime.hour * 3600
    minutes = ptime.minute * 60
    seconds = ptime.second
    microseconds = ptime.microsecond
    total_seconds = hours + minutes + seconds + (microseconds / 1000000)
    return round(total_seconds, 3)


def time_to_seconds_str(time_str):
    return f"{time_to_seconds(time_str):.03f}"


def seconds_str_to_time(seconds_str):
    milliseconds, seconds = modf(float(seconds_str))
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = seconds // 60
    seconds = seconds % 60
    milliseconds = int(round(milliseconds * 1000))
    return time(hour=hours, minute=minutes, second=seconds, microsecond=milliseconds * 1000)


def format_time(time_str):
    time_seconds = seconds_str_to_time(time_str)
    return time.strftime(time_seconds, args.time_fmt)[:-3]


def grouper(iterable, n, fillvalue=None):
    arguments = [iter(iterable)] * n
    return zip_longest(*arguments, fillvalue=fillvalue)


def get_files(input_fmt, output_fmt):
    for root, dirs, files in os.walk(args.input_dir, topdown=False):
        for file in files:
            if file.endswith(input_fmt):
                out_name = f"{'.'.join(file.split('.')[:-1])}.{output_fmt}"
                yield Entry(
                    basename=file,
                    dir_path=root,
                    filepath=Path(root) / file,
                    out_path=Path(args.output_dir) / out_name,
                    in_fmt=input_fmt,
                    out_fmt=output_fmt,
                )


def syncmap_to_dict(entry: Entry):
    with open(str(entry.filepath)) as syncmap:
        json_data = json.load(syncmap)

    return replace(entry, in_data=json_data['fragments'])


def srt_to_dict(entry: Entry):
    srt_data = []
    with open(str(entry.filepath)) as srt:
        for idx, time_slice, text, _ in grouper(srt, 4, ''):
            idx = int(idx)
            start, end = time_slice.split(' --> ')
            # remove trailing newline symbols '\n'
            end = end.rstrip()
            text = text.rstrip()

            # append syncmap entry
            srt_data.append({
                'begin': time_to_seconds_str(start),
                'children': [],
                'end': time_to_seconds_str(end),
                'id': f"f{idx:06d}",
                'language': 'lit',
                'lines': [text],
            })
    return replace(entry, out_data=srt_data)


def calculate_output_data(entry: Entry):
    out_data = []
    for idx, segment in enumerate(entry.in_data, start=1):
        start_time = format_time(segment['begin'])
        end_time = format_time(segment['end'])
        out_data.append({
            'id': idx,
            'start': start_time,
            'end': end_time,
            'text': segment['lines'][0],
        })
    return replace(entry, out_data=out_data)


def to_srt(entry: Entry):
    with open(entry.out_path, "w") as str_file:
        for segment in entry.out_data:
            print(f"{segment['id']}\n{segment['start']} --> {segment['end']}\n{segment['text']}\n", file=str_file)
    return entry.filepath


def to_syncmap(entry: Entry):
    with open(entry.out_path, "w") as syncmap_file:
        syncmap = {'fragments': entry.out_data}
        json.dump(syncmap, syncmap_file, indent=2)
    return entry.filepath


def convert_to_srt():
    input_observable = rx.from_iterable(get_files('json', 'srt'), pool_scheduler)
    input_observable.pipe(
        ops.map(syncmap_to_dict),
        ops.map(calculate_output_data),
        ops.map(to_srt),
    ).subscribe(
        on_next=lambda filename: print(f"Converted {filename}"),
        on_completed=lambda: print("Converting completed"),
        on_error=lambda err: print(f"ERROR: type: {type(err)}, message: {err}"),
    )


def convert_to_syncmaps():
    input_observable = rx.from_iterable(get_files('srt', 'json'), pool_scheduler)
    input_observable.pipe(
        ops.map(srt_to_dict),
        ops.map(to_syncmap),
    ).subscribe(
        on_next=lambda filename: print(f"Converted {filename}"),
        on_completed=lambda: print("Converting completed"),
        on_error=lambda err: print(f"ERROR: type: {type(err)}, message: {err}"),
    )


if __name__ == '__main__':
    args = parse_args()
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    optimal_thread_count = multiprocessing.cpu_count()
    pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

    if args.to_srt:
        convert_to_srt()
    else:
        convert_to_syncmaps()
