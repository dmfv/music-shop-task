# file to load data from sqlite file and provide some interfaces 

from sqlalchemy import (Column, MetaData, Table, Integer, String, create_engine, desc, func,
                        select, update, values)

# connect to existing database
engine = create_engine("sqlite:///music_shop.db", echo = False)
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
    band_songs = engine_connect.execute(songs.select().where(songs.c.band_id == band_id)).fetchall()        
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
        record_with_band_song = engine_connect.execute(music_records_songs.select().where(music_records_songs.c.song_id == song_id)).fetchall() # get all records with band songs
        for record in record_with_band_song:
            if record: # if record not empty list
                music_records_band_songs_ids.add(record[1]) # music_record_id - is second column
    if len(music_records_band_songs_ids) == 0: # if no records existing with songs of this band
        return []

    name_of_band_records = []
    for record_id in music_records_band_songs_ids:
        band_records_names = engine_connect.execute(music_records.select().where(music_records.c.music_record_id == record_id)).fetchall()         # get all songs from band
        if band_records_names: # if not empty list
            name_of_band_records.append(band_records_names[0][1])

    return name_of_band_records


# функция позволяющая показать лидеров продаж текущего года, то есть названия
# компакт-дисков, которые чаще всего покупали в текущем
# году  
def get_top_three_seller_records(engine_connect):
    records = engine_connect.execute(music_records.select().order_by(desc(music_records.c.sold_this_year))).fetchall()
    if len(records) == 0: # if there are no records in table
        return []
    top_seller_records_names = []
    for index in range(3):
        top_seller_records_names.append(records[index][1])
    return top_seller_records_names


# функция позволяющая вносить изменения данных о компакт-дисках и ввод
# новых данных
# def update_table_value(table, column_to_find, value_to_find, column_to_update, value_to_update, engine_connect):
    # engine_connect.execute(update(table).where(column_to_find == value_to_find).values(column_name_to_update = value_to_update))
def update_table_value(table_name, column_name, column_value, column_value_type, column_name_filter, column_value_filter, column_value_filter_type, engine_connect):
    if "string" in column_value_type.lower():
        column_value = str("'") + str(column_value) + str("'")
    if "string" in column_value_filter_type.lower():
        column_value_filter = str("'") + str(column_value_filter) + str("'")
    engine_connect.execute("UPDATE %s SET %s = %s WHERE %s = %s" % (table_name, column_name, column_value, column_name_filter, column_value_filter))

def add_column(table_name, column, engine):
    column_name = column.compile(dialect = engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute("ALTER TABLE %s ADD COLUMN %s %s" % (table_name, column_name, column_type))


# функция позволяющая предусмотреть вводить новые данных об ансамблях 
# (добавлять новые ансамбли можно и так через обычный insert)

# точно также можно добавить add_column и затем аналогичная функция update_table_value

###############################################################################################
# examples

# print(get_band_songs_number("Rammstein", connect))
# print(get_band_music_records_names("Pain", connect))

# print(get_top_three_seller_records(connect))

# update_table_value("music_records", "seller_name", "TOP asdasd", "String", "record_name", "first", "String", connect)
# connect.execute(update(music_records).where(music_records.c.record_name == "first").values(seller_name = "123")) # another way to do upper string

# column = Column("new_column_name", String(100), primary_key=True)
# add_column("music_records", column, engine)
