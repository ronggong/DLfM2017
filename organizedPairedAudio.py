"""
organize paired audio files into simannotator format
"""

from audioLyricsCsvParser import parseCorrespondingAriaCsv
from filepath import *
from src.textgridParser import textGrid2WordList
from lyricsMatch import stringDist
import soundfile as sf
import os
import csv

lines_dan = parseCorrespondingAriaCsv('./corresponding_arias/corresponding pro-amateur arias - dan.csv')
lines_laosheng = parseCorrespondingAriaCsv('./corresponding_arias/corresponding pro-amateur arias - laosheng.csv')

def saveAudio2Path(filename, audio, start_time, end_time, fs):
    start_sample = int(start_time*fs)
    end_sample = int(end_time*fs)
    # wavfile.write(filename, fs, audio[start_sample:end_sample])
    sf.write(filename, audio[start_sample:end_sample], fs)

def saveLyrics2Path(filename, lyrics):
    with open(filename, 'w') as testfile:
        csv_writer = csv.writer(testfile)
        csv_writer.writerow(lyrics)

def dictRubric():
    rubric = {'Zheng ti Overall': {'rubric': {'ratings': [1, 2, 3, 4]}},
              'Fa yin Pronunciation': {'rubric': {'ratings': [1, 2, 3, 4]}},
              'Yin diao Intonation': {'rubric': {'ratings': [1, 2, 3, 4]}},
              'Qiang ruo Loudness': {'rubric': {'ratings': [1, 2, 3, 4]}},
              'Yin se Tone quality': {'rubric': {'ratings': [1, 2, 3, 4]}}}
    return rubric

def dictSeg(start_time_overall,
            end_time_overall):
    seg = {'Zheng ti Overall': [{'start_time': start_time_overall,
                              'end_time': end_time_overall,
                              'label': 'Entire_sound'}],
            'Fa yin Pronunciation': [{'start_time': start_time_overall,
                                      'end_time': end_time_overall,
                                      'label': 'Entire_sound'}],
           'Yin diao Intonation': [{'start_time': start_time_overall,
                                     'end_time': end_time_overall,
                                     'label': 'Entire_sound'}],
           'Qiang ruo Loudness': [{'start_time': start_time_overall,
                                     'end_time': end_time_overall,
                                     'label': 'Entire_sound'}],
           'Yin se Tone quality': [{'start_time': start_time_overall,
                                     'end_time': end_time_overall,
                                     'label': 'Entire_sound'}]}
    return seg

def getFilenames(lines, role):
    dict_dataset_description = {}

    ii_exercise = 0
    for pair in lines:
        filename_current_ref_aria = pair[0]+'_'+pair[1]
        if pair[0] == role:
            path_wav = join(path_dataset_qmUpf_old,'wav')
            path_textgrid = path_textgrid_qmUpf_old
        else:
            path_wav = join(path_dataset_nacta_2017,'wav')
            path_textgrid = path_textgrid_nacta_2017

        filename_ref = pair[1]
        filename_amateur = pair[3]

        filename_ref_audio = join(path_wav, pair[0], filename_ref+'.wav')
        filename_ref_textgrid = join(path_textgrid, pair[0], filename_ref+'.textgrid')

        if pair[2] == role:
            path_wav = join(path_dataset_qmUpf_old,'wav')
            path_textgrid = path_textgrid_qmUpf_old
        else:
            path_wav = join(path_dataset_nacta_2017,'wav')
            path_textgrid = path_textgrid_nacta_2017

        filename_amateur_audio = join(path_wav, pair[2], filename_amateur + '.wav')
        filename_amateur_textgrid = join(path_textgrid, pair[2], filename_amateur + '.textgrid')


        audio_ref, fs_ref = sf.read(filename_ref_audio)

        audio_amateur, fs_amateur = sf.read(filename_amateur_audio)

        textgrid_line_ref = textGrid2WordList(filename_ref_textgrid, whichTier='line')
        textgrid_line_amateur = textGrid2WordList(filename_amateur_textgrid, whichTier='line')

        # clean the parsed lines
        textgrid_line_ref = [tlr for tlr in textgrid_line_ref if len(tlr[2])]
        textgrid_line_amateur = [tla for tla in textgrid_line_amateur if len(tla[2])]

        for ii_ref, line_element_ref in enumerate(textgrid_line_ref):
            name_exercise = pair[0] + '_' + filename_ref + '_' + str(ii_ref)
            name_exercise = name_exercise[-49:]
            for ii_amateur, line_element_amateur in enumerate(textgrid_line_amateur):
                if stringDist(line_element_ref[2], line_element_amateur[2]) > 0.7:

                    print(pair[0]+'_'+filename_ref+'_vs_'+pair[2]+'_'+filename_amateur, str(ii_ref), line_element_ref[2], line_element_amateur[2])
                    path_ref_amateur_saved_base = join('./corresponding_arias', role, pair[0]+'_' + filename_ref, str(ii_ref))
                    # + '_vs_' +pair[2]+'_'+ filename_amateur
                    path_ref_audio_saved = join(path_ref_amateur_saved_base, 'reference')
                    path_amateur_audio_saved = join(path_ref_amateur_saved_base, 'performances')

                    if not os.path.exists(path_ref_audio_saved):
                        os.makedirs(path_ref_audio_saved)
                    if not os.path.exists(path_amateur_audio_saved):
                        os.makedirs(path_amateur_audio_saved)

                    filename_ref_audio_saved = join(path_ref_audio_saved, pair[0]+'_' + filename_ref + '_' + str(ii_ref)+'.wav')

                    if not os.path.isfile(filename_ref_audio_saved):
                        # add exercise name to the dataset description dictionary
                        ii_exercise += 1

                        dict_dataset_description['exercise ' + str(ii_exercise)] = {
                            'name': name_exercise, 'recs': []}

                        saveAudio2Path(filename=filename_ref_audio_saved,
                                       audio=audio_ref,
                                       start_time=line_element_ref[0],
                                       end_time=line_element_ref[1],
                                       fs=fs_ref)

                        # add the ref_media value
                        dict_dataset_description['exercise '+str(ii_exercise)]['ref_media'] = filename_ref_audio_saved.replace('./corresponding_arias/'+role+'/', '')

                        # save the segmentation to json
                        dict_ref_seg = dictSeg(0,
                                               line_element_ref[1]-line_element_ref[0]-0.1
                                               )

                        json.dump(dict_ref_seg, open(filename_ref_audio_saved.replace('.wav', '.trans_json'), 'w'))

                    filename_amateur_audio_saved = join(path_amateur_audio_saved, pair[2] + '_' + filename_amateur + '_' + str(ii_amateur) + '.wav')
                    saveAudio2Path(filename=filename_amateur_audio_saved,
                                   audio=audio_amateur,
                                   start_time=line_element_amateur[0],
                                   end_time=line_element_amateur[1],
                                   fs=fs_amateur)

                    # find the key for the ref name, write the path into recs key
                    key_exercise = None
                    for key in dict_dataset_description:
                        if dict_dataset_description[key]['name'] == name_exercise:
                            key_exercise = key

                    # add the rec value
                    name_rec = pair[2]+'_'+filename_amateur+'_'+str(ii_amateur)
                    name_rec = name_rec[-49:]
                    dict_dataset_description[key_exercise]['recs'].append({'_id': name_rec,
                                                                            'path': filename_amateur_audio_saved.replace('./corresponding_arias/'+role+'/', '')})

                    saveLyrics2Path(filename=join(path_ref_amateur_saved_base, 'lyrics_'+ pair[2]+'_'+filename_amateur+'_'+str(ii_amateur)+'.csv'),
                                    lyrics=[line_element_ref[2], line_element_amateur[2]])

                    # save the segmentation to json
                    dict_amateur_seg = dictSeg(0,
                                               line_element_amateur[1]-line_element_amateur[0]-0.1
                                               )

                    json.dump(dict_amateur_seg, open(filename_amateur_audio_saved.replace('.wav', '.json'), 'w'))

    return dict_dataset_description

if __name__ == '__main__':
    import json
    dict_data_description_laosheng = getFilenames(lines_laosheng, 'laosheng')
    json.dump(dict_data_description_laosheng,
              open(join('./corresponding_arias/laosheng', 'data.json'), 'w'))
    json.dump(dictRubric(),
              open(join('./corresponding_arias/laosheng', 'rubric.json'), 'w'))

    dict_data_description_danAll = getFilenames(lines_dan, 'danAll')
    json.dump(dict_data_description_danAll,
              open(join('./corresponding_arias/danAll', 'data.json'), 'w'))
    json.dump(dictRubric(),
                open(join('./corresponding_arias/danAll', 'rubric.json'), 'w'))

