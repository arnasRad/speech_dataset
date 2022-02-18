import os
import re
from pathlib import Path

if __name__ == "__main__":
    input_dir = "/media/arnas/SSD Disk/inovoice/unzipped/child_voice"
    txt_files = [Path(root) / file
                 for root, dirs, files in os.walk(input_dir)
                 for file in files
                 if file.endswith('txt')]

    for txt in txt_files:
        with open(txt, mode='r', encoding='utf-8') as f:
            text = f.read()

        text = re.sub('\n{2,}', '\n', text)
        text = re.sub('\n', '\n\n', text)

        with open(txt, mode='w', encoding='utf-8') as f:
            f.write(text)
        print(f"Written {txt}")
