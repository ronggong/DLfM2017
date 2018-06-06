# -*- coding: utf-8 -*-

from filepath import *
import os
import csv
import json
from jingjuScores import getMelodicLine
import fractions


def floatOrFraction(strValue):
    '''str --> fractions.Fraction or float
    Given a numeric value as a string, it returns it as a fractions.Fraction
    object if contains '/' on it, or as a float otherwise
    '''
    if '/' in strValue:
        numerator = int(strValue.split('/')[0])
        denominator = int(strValue.split('/')[1])
        value = fractions.Fraction(numerator, denominator)
    elif len(strValue) == 0:
        value = None
    else:
        value = float(strValue)

    return value

def parseAudioLyrics(filename_audio_csv, filename_audio_json):

    dict_lines = {}
    with open(filename_audio_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        ii_row = 0
        for row in reader:
            if row[0] != "Path name":
                print(row)
                dict_lines[ii_row] = row[6]
            ii_row += 1

    with open(filename_audio_json, 'w') as outfile:
        json.dump(dict_lines, outfile)

def parseCorrespondingAriaCsv(filename_audio_csv):

    lines = []
    with open(filename_audio_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        ii_row = 0
        for row in reader:
            if row[0] != "Path name pro":
                # print(row)
                lines.append([row[0], row[1], row[2], row[3]])
            ii_row += 1

    return lines

def getDictScoreInfo(score_info_filepath):
    """
    dictionary {path name_aria_name: [line_info]}
    line_info: [lineNumber, lyrics, filenameScore, startEndOffset]
    :param score_info_filepath:
    :return:
    """
    dict_score_info = {}
    with open(score_info_filepath, 'r') as csvfile:
        score_info = csv.reader(csvfile, delimiter=",")

        aria_name_old = ''
        path_name_old = ''
        line_number = 0
        for row in score_info:
            if row[0] != 'Path name':
                path_name = row[0]
                if len(path_name):
                    path_name_old = path_name
                if len(row[7]):
                    aria_name = row[1]
                    if len(aria_name):
                        # row[0] != empty
                        line_number = 0
                        aria_name_old = aria_name
                        dict_score_info[path_name_old+'_'+aria_name_old] = []
                    else:
                        line_number += 1

                    try:
                        dict_score_info[path_name_old+'_'+aria_name_old].append({'lineNumber': line_number,
                                                               'lyrics': row[7],
                                                               'filenameScore':row[8],
                                                               'startEndOffset': [row[9],
                                                                                  row[10]]})
                    except ValueError:
                        print(aria_name_old + '_' + str(line_number) + ' ' + 'valueError: ' + row[7] + ' ' + row[8])

    return dict_score_info

def getScores(dict_score_info):
    """
    Read score info dictionary, parse score lines including both notes and rests, output:
    dictionary: {pathName_ariaName:list_line, ...}
    list_line: [[note0, note1, ...], line1, ...]
    note: {freq, lyric, quarterLength}
    :param dict_score_info:
    :return:
    """
    dict_scores = {}
    for pathName_ariaName in dict_score_info:
        lines = []
        list_line = dict_score_info[pathName_ariaName]
        for line in list_line:
            score_filename = line['filenameScore']
            start = line['startEndOffset'][0]
            end = line['startEndOffset'][1]
            score_file_path = os.path.join(score_path,score_filename)
            start = start.replace(',', '.')
            end = end.replace(',', '.')
            start = floatOrFraction(str(start))
            end = floatOrFraction(str(end))
            line_score = getMelodicLine(score_file_path, start, end, show=False)

            notes = []
            for note in line_score.flat.notesAndRests.stream():
                if note.isNote:
                    notes.append({'freq':note.pitch.freq440,'lyric':note.lyric,'quarterLength':float(note.quarterLength)})
                else:
                    notes.append({'freq':None,'lyric':None,'quarterLength':float(note.quarterLength)})

            lines.append(notes)
        dict_scores[pathName_ariaName] = lines
    return dict_scores
    # return dict_score_info

def dictScores2durationCsv(dict_scores):
    """
    Read dcit_scores, save each score lyrics and durations into a .csv
    :param dict_scores:
    :return:
    """
    for pathName_ariaName in dict_scores:
        pathName = pathName_ariaName.split('_')[0]
        ariaName = pathName_ariaName.replace(pathName + '_', '')

        if '2017' in pathName:
            pathName = os.path.join(score_duration_path, pathName)
            if not os.path.isdir(pathName):
                os.mkdir(pathName)
        else:
            pathName = score_duration_path


        list_aria = []
        max_length = 0
        for ii_line, line in enumerate(dict_scores[pathName_ariaName]):
            line_lyric = ['']
            line_duration = [60]
            for note in line:
                if note['lyric']:
                    line_lyric.append(note['lyric'])
                    line_duration.append(note['quarterLength'])
                else:
                    line_duration[-1] += note['quarterLength']
            list_aria.append(line_lyric)
            list_aria.append(line_duration)
            if max_length < len(line_lyric):
                max_length = len(line_lyric)

        with open(os.path.join(pathName, ariaName+'.csv'), 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for line in list_aria:
                writer.writerow(line+['']*(max_length-len(line)))


if __name__ == '__main__':
    filename_audio_csvs = [
        # './lyrics_audio/line metadata all - pro-laosheng.csv',
        #                   './lyrics_audio/line metadata all - pro-dan.csv',
                          './lyrics_audio/line metadata all - amateur-laosheng.csv',
                          # './lyrics_audio/line metadata all - amateur-dan.csv',
    ]
    # filename_audio_json = './lyrics_audio/line metadata all - pro-laosheng.json'
    # parseAudioLyrics(filename_audio_csv, filename_audio_json)
    for filename_audio_csv in filename_audio_csvs:
        dict_score_info = getDictScoreInfo(filename_audio_csv)
        dict_scores = getScores(dict_score_info)
        dictScores2durationCsv(dict_scores)