#! /Users/geoff/mg-loader/venv/bin/python3

import os
import sys

import pydub
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='mg-loader',
        description='Prepares samples and auto-loads them onto a MicroGranny SD card',
        epilog='Created by Geoff Unger')
    parser.add_argument('path')
    args = parser.parse_args()
    path = args.path
    if (os.path.isdir(path)):
        print(f'Directory found: {path}')
        with os.scandir(path) as files:
            for file in files:
                if (os.path.isfile(file)):
                    addSample(file)
    else:
        addSample(path)
    print("Done!")

def addSample(fileName):
    if os.path.splitext(fileName)[1] not in ['.wav', '.mp3', '.WAV', '.MP3']:
        return
    if os.path.splitext(fileName)[1] in ['.wav', '.WAV']:
        sample = pydub.AudioSegment.from_wav(fileName)
    if os.path.splitext(fileName)[1] in ['.mp3', '.MP3']:
        sample = pydub.AudioSegment.from_mp3(fileName)
    print(f'Processing sample: {fileName}')
    sample = sample.set_channels(1)
    pydub.effects.normalize(sample)
    sample = sample.set_frame_rate(22050)
    sample.set_sample_width(2)
    filename = find_next_filename()
    sample.export('/Volumes/MG/' + filename, format='wav')
    print(f'Saved under filename: {filename}')


def find_next_filename():
    existing_files = []
    try:
        with os.scandir('/Volumes/MG') as entries:
            for entry in entries:
                existing_files.append(entry.name)
    except:
        print('Error - SD card not found!')
        sys.exit(1)
    char_num_list = []
    for num in range(1,10):
        char_num_list.append(str(num))
    for char in range(65, 91):
        char_num_list.append(chr(char))
    for char1 in range(65,91):
        for char2 in char_num_list:
            filename = chr(char1) + char2 + '.WAV'
            if filename not in existing_files:
                return filename

 # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
