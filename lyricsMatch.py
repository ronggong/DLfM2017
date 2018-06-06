# -*- coding: utf-8 -*-

# from filepath import *
import json

def stringDist(str0,str1):
    '''
    utf-8 format string
    :param str0:
    :param str1:
    :return:
    '''

    intersection = [val for val in str0 if val in str1]

    dis = len(intersection)/float(max(len(str0), len(str1)))

    return dis

def matchLyrics(filename_score_json, filename_audio_json, filename_audio_score_match_json):
    with open(filename_score_json) as outfile:
        list_score = json.load(outfile)


    with open(filename_audio_json) as outfile:
        list_audio = json.load(outfile)

    for num in list_audio:
        for line_lyrics_score in list_score:
            dist = stringDist(list_audio[num], line_lyrics_score)
            if dist > 0.6:
                list_audio[num] = [list_audio[num]] + [line_lyrics_score] + list_score[line_lyrics_score]

    with open(filename_audio_score_match_json, 'w') as outfile:
        json.dump(list_audio, outfile)