# find counterpart lyrics in score lyrics for a cappella singing lyrics


from scoreCsvParser import parseScore
from audioLyricsCsvParser import parseAudioLyrics
from lyricsMatch import matchLyrics
from concatenateCsv import concateCsv

##-- parse score line in lines_data.json
# parseScore()

filename_score_json = "./lines_data.json"
filename_audio_csv  = "./lyrics_audio/line metadata all - pro-laosheng.csv"
filename_audio_json  = "./lyrics_audio/line metadata all - pro-laosheng.json"
filename_audio_score_match_json = "./lyrics_audio/line metadata all score - pro-laosheng.json"
filename_audio_csv_new  = "./lyrics_audio/line metadata all score - pro-laosheng.csv"


##-- parse lyrics of a cappella singing
parseAudioLyrics(filename_audio_csv, filename_audio_json)

##-- match the above two lyrics
matchLyrics(filename_score_json, filename_audio_json, filename_audio_score_match_json)

##-- concatenate the counterpart lyrics of score lyrics line to a cappella one
concateCsv(filename_audio_csv, filename_audio_score_match_json, filename_audio_csv_new)

