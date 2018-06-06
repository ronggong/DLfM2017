# find the lines in csv which can not correspond in the textgrid
import csv
import os
from lyricsMatch import stringDist

def parseAudioLyrics(filename_audio_csv):

    dict_lines = {}
    with open(filename_audio_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        ii_row = 0
        for row in reader:
            if row[0] != "Path name":
                dict_lines[ii_row] = row
            ii_row += 1
    return dict_lines

def parseLyricsCsv(filename_lyrics_csv):
    lyrics = []
    with open(filename_lyrics_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            lyrics.append(row[0])
    return lyrics


# find score textgrid phrase split difference
dict = parseAudioLyrics('./lyrics_audio/line metadata all - amateur-laosheng.csv')

old_path_name = ''
old_file_name = ''
path_name = ''
lyrics = None
for num_line in dict:
    line = dict[num_line]
    if len(line[6]):
        found_lyrics = False
        new_path_name = line[0]
        new_file_name = line[1]
        if len(new_path_name):
            path_name = new_path_name
        if len(new_file_name):
            file_name = new_file_name
            if '2017' in path_name:
                lyricsCsv = os.path.join('./lyrics_audio/lyrics_textgrid_olddataset', path_name, new_file_name+'.textgrid.csv')
            else:
                lyricsCsv = os.path.join('./lyrics_audio/lyrics_textgrid_olddataset', file_name+'.csv')
            try:
                # print(lyricsCsv)
                lyrics = parseLyricsCsv(lyricsCsv)
                # print(lyrics)
            except FileNotFoundError:
                lyrics = None
        if lyrics is not None:
            for l in lyrics:
                if stringDist(l, line[6]) > 0.8:
                    found_lyrics = True
            if not found_lyrics:
                print(num_line, path_name, file_name, line[6])

