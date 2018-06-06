# find the amateur a cappella singing lyrics which correspond to those in professional lyrics

from lyricsMatch import stringDist
import json
import csv

filename_audio_csv_pro  = "./lyrics_audio/line metadata all - pro-dan.csv"
filename_audio_json_pro  = "./lyrics_audio/line metadata all - pro-dan.json"
filename_audio_json_amateur = "./lyrics_audio/line metadata all - amateur-dan.json"
filename_pro_amateur_json = "./lyrics_audio/line metadata all - pro-amateur-dan.json"
filename_pro_amateur_csv = "./lyrics_audio/line metadata all - pro-amateur-dan.csv"

def matchLyrics():
    with open(filename_audio_json_pro) as outfile:
        list_pro = json.load(outfile)

    with open(filename_audio_json_amateur) as outfile:
        list_amateur = json.load(outfile)

    # print(list_pro)
    list_pro_amateur = {}
    for num_pro in list_pro:
        for num_amatuer in list_amateur:
            try:
                dist = stringDist(list_pro[num_pro], list_amateur[num_amatuer])
            except:
                print(list_pro[num_pro], list_amateur[num_amatuer])

            if dist > 0.6:
                try:
                    list_pro_amateur[num_pro] = list_pro_amateur[num_pro] + [num_amatuer] + [list_amateur[num_amatuer]]
                except:
                    list_pro_amateur[num_pro] = [list_pro[num_pro]] + [num_amatuer] + [list_amateur[num_amatuer]]
        try:
            print(list_pro_amateur[num_pro])
        except:
            list_pro_amateur[num_pro] = list_pro[num_pro]

    with open(filename_pro_amateur_json, 'w') as outfile:
        json.dump(list_pro_amateur, outfile)

def concateCsv():

    with open(filename_pro_amateur_json) as outfile:
        dict_pro_amateur = json.load(outfile)

    len_value = 0
    for value in dict_pro_amateur.values():
        if not isinstance(value, str):
            if len(value)-1 > len_value:
                len_value = len(value)-1


    with open(filename_pro_amateur_csv, 'w', newline='', encoding='utf-8') as csvfile_write:
        csv_writer = csv.writer(csvfile_write, delimiter=',')

        with open(filename_audio_csv_pro, 'r', encoding='utf-8') as csvfile_read:
            reader = csv.reader(csvfile_read, delimiter=',')
            ii_row = 0
            for row in reader:
                if ii_row != 0:
                    if isinstance(dict_pro_amateur[str(ii_row)], str):
                        csv_writer.writerow(row + [""]*len_value)
                    else:
                        csv_writer.writerow(row + dict_pro_amateur[str(ii_row)][1:])
                ii_row += 1

matchLyrics()
concateCsv()