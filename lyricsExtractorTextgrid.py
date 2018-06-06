from textgridParser import textGrid2WordList
from filepath import *
import os
import csv

def getRecordings(wav_path):
    """
    retrieve the filename from wav_path
    :param wav_path: not necessarily only contain .wav
    :return:
    """
    recordings      = []
    for root, subFolders, files in os.walk(wav_path):
            for f in files:
                file_prefix, file_extension = os.path.splitext(f)
                if file_prefix != '.DS_Store' and file_prefix != '_DS_Store':
                    recordings.append(file_prefix)

    return recordings


def lyrics_textgrid_csvwriter(filenames_textgrid, textgrid_path, path_to_save, extension=''):


    for fn in filenames_textgrid:
        fn_full = os.path.join(textgrid_path, fn+extension)
        list_line = textGrid2WordList(fn_full, whichTier='line')

        fn_csv = os.path.join(path_to_save, fn+'.csv')
        with open(fn_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for line in list_line:
                if len(line[2]):
                    writer.writerow([line[2]])

filenames_textgrid = getRecordings(textgrid_path_dan)

lyrics_textgrid_csvwriter(filenames_textgrid, textgrid_path_dan, './lyrics_audio/lyrics_textgrid_olddataset', '.textgrid')

# for path_new in os.walk(dataset_path_new):
#     if len(path_new[1]) == 0:
#         lyrics_textgrid_csvwriter(path_new[2], path_new[0],
#                                   os.path.join('./lyrics_audio/lyrics_textgrid_olddataset', path_new[0].split('/')[-1]))