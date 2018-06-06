# from filepath import *
import json
import csv

def concateCsv(filename_audio_csv, filename_audio_score_match_json, filename_audio_csv_new):

    with open(filename_audio_score_match_json) as outfile:
        dict_audio_score_match = json.load(outfile)


    with open(filename_audio_csv_new, 'w', newline='', encoding='utf-8') as csvfile_write:
        csv_writer = csv.writer(csvfile_write, delimiter=',')

        with open(filename_audio_csv, 'r', encoding='utf-8') as csvfile_read:
            reader = csv.reader(csvfile_read, delimiter=',')
            ii_row = 0
            for row in reader:
                if ii_row != 0:
                    if isinstance(dict_audio_score_match[str(ii_row)], str):
                        csv_writer.writerow(row + ["", "", "", ""])
                    else:
                        csv_writer.writerow(row + dict_audio_score_match[str(ii_row)][1:])
                ii_row += 1