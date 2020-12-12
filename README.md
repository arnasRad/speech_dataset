# Introduction

speech_dataset is just a tool to help build speech datasets for neural network training. It's is based on this [tutorial](https://medium.com/@klintcho/creating-an-open-speech-recognition-dataset-for-almost-any-language-c532fb2bc0cf). It's is not fully automated and will require a lot of manual editing. Below is a tutorial for building the speech dataset using this tool. Note that with some pairs of ebooks and audiobooks, there may be undocumented steps that the user may need to cover on his own to successfully build a dataset.

# Prerequisites:

* [Notepad++](https://notepad-plus-plus.org/downloads/)
* [Calibre](https://calibre-ebook.com/download) (if ebook format is .epub)
* [Adobe Acrobat Pro DC](https://get.adobe.com/reader/) (if ebook format is .pdf)
* [Audacity](https://www.audacityteam.org/download/)
* [eSpeak](https://www.vultr.com/docs/install-espeak-on-ubuntu-18-04)
    * sudo apt-get install espeak
* [Aeneas](https://github.com/readbeyond/aeneas/blob/master/wiki/INSTALL.md)
    * wget https://raw.githubusercontent.com/readbeyond/aeneas/master/install_dependencies.sh
    * bash install_dependencies.sh
    * pip install aeneas

# Steps to creating dataset

## Manual Part

1. Convert the book to `.txt` format
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
2. Manually preprocess .txt file using preferred text editor (I'm using Notepad++)
   1. Remove the book introduction and ending parts
      - text must start with start of chapter 1 and end of the last chapter
   2. Make sure that each paragraph is separated by two new lines `\n\n`
      - replace all triple new lines `\n\n\n` with one new line `\n`
      - in case there are only one new line between paragraphs - replace all `\n\n` with `\n` and then add additional `\n` after each new line in the file
   3. Remove trailing new lines at the start and end of the file
   4. Check if ebook has any foot-notes
      - search ebook for `*` symbol or digits that follow text.
      - if foot-notes found - listen to audio at that part and edit the text so that it matches the audio
   5. There may be foreign language sentences in text that the speaker does not record. Consider manually finding these sentences and edit the text so that it matches audio
   6. Make sure that there are no page numerations left
   7. Replace all digits with their word representations
   8. Remove all inaudible abbreviations (usually they're name abbreviations, e.g. replace J. K. Rowling with Rowling)
   9. Expand audible abbreviations (list of possible abbreviations for Lithuanian language is in abbreviations.txt file)
   10. Remove page headers and footers if such exists
3. Preprocess audio files
   1. import audio files to Audacity
   2. trim start of audiobook (book introduction, release date etc.)
   3. trim end of audiobook (ending notes, credits etc.)
   4. trim start of each audio (speaker tells what's the section number)
   5. trim end of each audio (silence trimming)
   6. export audios in 22050 sample rate
   7. name each audio file as ***audio-index.mp3***, where index stands for corresponding audio chapter
4. Split ebook to chapters to match audio files' start and end
   - name each `.txt` file `chapter-index.txt` where `index` is the number of audio matching the text
5. Place the resulting files to their corresponding folders
   - place text files in `speech_dataset/books/book_name/text`
   - place audio files in `speech_dataset/books/book_name/audio`
	
## Automated part

1. In `properties.py` file: set values for `book_list` (names of the folders containing book data) and `chapter_count_in` (chapter count of each book).
2. Force align chapters using `alignment.py`.
   - Calculations may fail at some chapter. It may be due to operating systems that the programs is running on (Windows users experience this problem more often), poor quality data (text is not an accurate transcription of audio) or that chapter size is too big. Set start_book and start_chapter variable values to ones that the calculations stopped at, restart the script and it should run just fine. If error persists - try splitting the chapters to smaller chunks or cleaning the data.
   - You can validate alignment results using a simple third-party GUI - [finetuneas](https://github.com/ozdefir/finetuneas).
3. Export dataset using `export_dataset.py`