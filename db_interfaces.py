# file to load data from sqlite file and provide some interfaces 

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, func, select

# connect to existing database
engine = create_engine('sqlite:///music_shop.db', echo = False)
meta = MetaData(engine)

# load data from tables
musicians = Table("musicians", meta, autoload = True)
bands = Table("bands", meta, autoload = True)
songs = Table("songs", meta, autoload = True)
music_records = Table("music_records", meta, autoload = True)
music_records_songs = Table("music_records_songs", meta, autoload = True)

connect = engine.connect()

def get_band_id(band_name, engine_connect):
    band_list = connect.execute(bands.select().where(bands.c.name == band_name)).fetchall()
    if len(band_list) == 0: # if band name not correct or not existing
        return 0
    band_id = band_list[0][0]
    return band_id

# функция позволяющая получить количество музыкальных произведений заданного ансамбля
def get_band_songs_number(band_name, engine_connect):
    band_id = get_band_id(band_name, engine_connect)
    req = select([func.count()]).select_from(songs).where(songs.c.band_id == band_id)
    songs_number = engine_connect.execute(req).fetchall()[0][0]
    return songs_number

# функция позволяющая выводить название всех компакт-дисков заданного ансамбля
def get_band_music_records_names(band_name, engine_connect):
    band_id     = get_band_id(band_name, engine_connect)
    # get all songs from band
    band_songs = connect.execute(songs.select().where(songs.c.band_id == band_id)).fetchall()        
    if len(band_songs) == 0: # check if songs existing
        return []

    # get list of all song's ids from this band
    band_songs_ids = []
    for song in band_songs:
        if song: # if non zeros array
            band_songs_ids.append(song[0])
    if len(band_songs_ids) == 0:
        return []
    
    # get all records id with band's songs
    music_records_band_songs_ids = set() # set because two (or more) records can have the same songs
    for song_id in band_songs_ids:
        # get all records with one song song_id
        record_with_band_song = connect.execute(music_records_songs.select().where(music_records_songs.c.song_id == song_id)).fetchall() # get all records with band songs
        for record in record_with_band_song:
            if record: # if record not empty list
                music_records_band_songs_ids.add(record[1]) # music_record_id - is second column
    if len(music_records_band_songs_ids) == 0: # if no records existing with songs of this band
        return []

    name_of_band_records = []
    for record_id in music_records_band_songs_ids:
        band_records_names = connect.execute(music_records.select().where(music_records.c.music_record_id == record_id)).fetchall()         # get all songs from band
        if band_records_names: # if not empty list
            name_of_band_records.append(band_records_names[0][1])

    return name_of_band_records


# функция позволяющая показать лидеров продаж текущего года, то есть названия
# компакт-дисков, которые чаще всего покупали в текущем
# году

# функция позволяющая вносить изменения данных о компакт-дисках и ввод
# новых данных

# функция позволяющая предусмотреть вводить новые данных об ансамблях 
# (добавлять новые ансамбли можно и так через обычный insert)