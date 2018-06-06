# -*- coding: utf-8 -*-

from filepath import *
import csv
import json

def parseScore():
    dict_lines = {}
    with open(filename_score_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0]:
                filename_xml = row[0]
            dict_lines[row[5]] = [filename_xml, row[6], row[7]]


    with open(filename_score_json, 'w') as outfile:
        json.dump(dict_lines, outfile)