filename_score_csv = "/Users/gong/Documents/pycharmProjects/Jingju-Score-Analysis/scores/lines_data.csv"
filename_score_json = "./lines_data.json"

filename_audio_csv = "./lyrics_audio/lyrics - amateur-laosheng.csv"
filename_audio_json = "./lyrics_audio/lyrics - amateur-laosheng.json"

filename_audio_score_match_json = "./lyrics_audio/lyrics_score - amateur-laosheng.json"
filename_audio_csv_new = "./lyrics_audio/lyrics - amateur-laosheng_new.csv"

score_path = './scores_all'
score_duration_path = './scores_duration'

from os.path import join
dataset_path = '/Users/gong/Documents/MTG document/Jingju arias/jingju_a_cappella_singing_dataset_extended_nacta2017/textgrid'
dataset_path_new = '/Users/gong/Documents/MTG document/Jingju arias/jingju_a_cappella_singing_dataset_extended_nacta2017/annotations'
textgrid_path_dan           = join(dataset_path,'danAll')
textgrid_path_laosheng      = join(dataset_path,'qmLonUpf/laosheng')

path_dataset_qmUpf_old = '/Users/gong/Documents/MTG document/Jingju arias/jingju_a_cappella_singing_dataset'
path_dataset_nacta_2017 = '/Users/gong/Documents/MTG document/Jingju arias/jingju_a_cappella_singing_dataset_extended_nacta2017'

path_textgrid_qmUpf_old = join(path_dataset_qmUpf_old, 'textgrid')
path_textgrid_nacta_2017 = join(path_dataset_nacta_2017, 'textgridDianSilence')