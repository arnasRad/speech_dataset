#Introduction

speech_dataset is just a tool to help build speech datasets for neural network training. Its is based on this [tutorial](https://medium.com/@klintcho/creating-an-open-speech-recognition-dataset-for-almost-any-language-c532fb2bc0cf). Its is not fully automated and will require a lot of manual editing. Below is a tutorial for building the speech dataset using this tool. Note that there may be undocumented steps with some pairs of ebooks and audiobooks that the user may need to cover on his own to successfully build a dataset.

#Prerequisites:

* [Notepad++](https://notepad-plus-plus.org/downloads/)
* [Calibre](https://calibre-ebook.com/download) (if ebook format is .epub)
* [Adobe Acrobat Pro DC](https://get.adobe.com/reader/) (if ebook format is .pdf)
* [Audacity](https://www.audacityteam.org/download/)
* [Aeneas](https://github.com/readbeyond/aeneas/blob/master/wiki/INSTALL.md)

#Steps to creating dataset

##Manual Part

1. Download an ebook
2. Convert the book to `.txt` format
   - If book format is `.epub`:
     1. open `Calibre`
     2. import the book to convert
     3. select the book
     4. click `Convert Books` (liet. Konvertuoti knygas)
     5. choose `TXT` output format
     6. click `OK` (liet. Gerai)
   - If book format is .pdf:
     1. open `Adobe Acrobat Pro DC`
     2. open `View -> Tools -> Export PDF`
     3. select `More Formats -> Text (Plain)`
     4. Click on settings icon next to `Text (Plain)` label
     5. Select `Encoding = UTF-8` and click `OK`
     6. Click `Export`
3. Manually preprocess .txt file using preferred text editor (I'm using Notepad++); see [Regex notes](#Regex-notes)
   1. Remove the book introduction and ending parts
      - text must start with start of chapter 1 and end of the last chapter
   2. Make sure that each paragraph is separated by two new lines `\n\n`
      - replace all triple new lines `\n\n\n` with on new line `\n`
      - in case there are only one new line between paragraphs - replace all `\n\n` with `\n` and then add additional `\n` after each new line in the file
   3. Remove trailing new lines at the start and end of the file
   4. Check if ebook has any footer explanations
      - search ebook for `*` symbol.
      - if footer explanations found - listen to audio at that part and edit the text so that it matches the audio
   5. there may be foreign language sentences in text that the speaker does not record. Consider manually finding these sentences and edit the text so that it matches audio
4. preprocess audio files
   1. import audio files to Audacity
   2. trim start of audiobook (book introduction, release date etc.)
   3. trim end of audiobook (ending notes, credits etc.)
   4. trim start of each audio (speaker tells what's the section number)
   5. trim end of each audio (silence trimming)
5. using audacity, split ebook to chapters to match audio files' start and end
   - name each `.txt` file `chapter-index.txt` where `index` is the number of audio matching the text
6. place the resulting text files to `speech_dataset/books/speaker_name/book_name/text/original`
7. place the resulting audio files to `speech_dataset/books/speaker_name/book_name/audio/long`
	
##Semi-automated part

1. In `properties.py` file: set values for `book_chapter_count` and `book_dir` (relative directory of book containing audio and text files)
2. Preprocess chapters using `chapter_preprocess.py`
3. Check the split chapters text and (manually) determine time in audio chapters where split occurs
4. In `properties.py` file: set `split_book_chapters` (index of chapters that were split) and `audio_split_marks` (time in minutes and seconds that audio should be split on)
5. Run `audio_preprocess.py` with `export_without_splitting` parameter set to `True`
6. Check if split audio files match text files. If not - adjust `audio_split_marks` in `properties.py` and repeat step 5 with `export_without_splitting` parameter set to `False`
7. Preprocess text to `aeneas` text format using `aeneas_preprocess.py`
8. Manually check the files if there are no lines containing only non-letter symbols; remove if any is found
9. Force align chapters text and audio using `aeneas_forced_alignment.py`
   - Calculations may fail at some chapter. In that case - adjust the loop range start with index of chapter that the error occurred on. Loop expression in `main()` method to modify:
     `for chapter in range(chapter_index, properties.book_chapter_count + 1)`
10. Export dataset using `export_dataset.py`
11. (optional). If intending to process further audio books: in `properties.py` - adjust `dataset_last_chapter_index` to append future audiobooks to dataset. ***if not set - dataset will be overwritten by the new book***
12. Before using the dataset for training - remove headers from `metadata.csv`

##Regex notes
1. Page break has split a sentence mid-way
   - *\p{Ll} - unicode lowercase letter that has an uppercase variant*
   - *\p{L} - unicode letter*
    ```
    (\p{L})\n+(\p{Ll})
    ```
    ```
    ([- ])\n+(\p{Ll})
    ```
2. Page break has split a word mid-way
    ```
    (\p{L})\s*\-\s*(\p{Ll})
    ```
3. Year range not separated by whitespaces
    ```
    [0-9]{4}\-[0-9]{4}
   ```
4. After aeneas preprocessing: line starts with multiple dots
    ```
    \n([.]{1,4})\s*([.]{1,4})\s*
   ```
