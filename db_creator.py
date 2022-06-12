# table structure creator
from datetime   import date
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, Date

engine = create_engine("sqlite:///music_shop.db", echo = False)
meta = MetaData()

# basic tables for database
musicians = Table(
   "musicians", meta, 
   Column("musician_id", Integer, primary_key = True), 
   Column("first_name",  String), 
   Column("last_name",   String), 
   Column("band_id",     Integer, ForeignKey("bands.band_id")), 
   Column("role",        String), 
)

bands = Table(
   "bands", meta, 
   Column("band_id", Integer, primary_key = True), 
   Column("name",    String), 
)

songs = Table(
   "songs", meta, 
   Column("song_id", Integer, primary_key = True), 
   Column("band_id", Integer, ForeignKey("bands.band_id")), 
   Column("name",    String), 
)

music_records = Table(
   "music_records", meta, 
   Column("music_record_id",    Integer, primary_key = True), 
   Column("producer_name",      String), 
   Column("seller_name",        String), 
   Column("wholesale_price",    Integer),
   Column("retail_price",       Integer), 
   Column("creation_date",      Date),
   Column("number_of_copies",   Integer), 
   Column("sold_previous_year", Integer), 
   Column("sold_this_year",     Integer),
   Column("number_of_unsold",   Integer),
)

music_records_songs = Table(
   "music_records_songs",    meta, 
   Column("song_id",         Integer, ForeignKey("songs.song_id")),
   Column("music_record_id", Integer, ForeignKey("music_records.music_record_id")),
)

# connect to database and create all tables
connect = engine.connect()
meta.create_all(engine)

# insert sampels to tables
# bands
connect.execute(bands.insert().values(name = "Rammstein"))
connect.execute(bands.insert().values(name = "Pain"))
connect.execute(bands.insert().values(name = "Eisbrecher"))
Rammstein_id   = connect.execute(bands.select().where(bands.c.name == "Rammstein")).fetchall()[0][0]
Pain_id        = connect.execute(bands.select().where(bands.c.name == "Pain")).fetchall()[0][0]
Eisbreacher_id = connect.execute(bands.select().where(bands.c.name == "Eisbrecher")).fetchall()[0][0]

# musicians
connect.execute(musicians.insert().values(first_name = "Till",      last_name = "Lindemann", role = "Vocal",  band_id = Rammstein_id))
connect.execute(musicians.insert().values(first_name = "Paul",      last_name = "Landers",   role = "Guitar", band_id = Rammstein_id))
connect.execute(musicians.insert().values(first_name = "Peter",     last_name = "Tägtgren",  role = "Мocal",  band_id = Pain_id))
connect.execute(musicians.insert().values(first_name = "Alexander", last_name = "Wesselsky", role = "Vocal",  band_id = Eisbreacher_id))

# songs
connect.execute(songs.insert().values(band_id = Rammstein_id,   name = "Raise Raise"))
connect.execute(songs.insert().values(band_id = Rammstein_id,   name = "Zick Zack"))
connect.execute(songs.insert().values(band_id = Pain_id,        name = "Party in My Head"))
connect.execute(songs.insert().values(band_id = Pain_id,        name = "Same Old Song"))
connect.execute(songs.insert().values(band_id = Eisbreacher_id, name = "Eisbrecher"))
connect.execute(songs.insert().values(band_id = Eisbreacher_id, name = "Was ist hier los?"))

# music records
connect.execute(music_records.insert().values(producer_name     = "Motor Music",   
                                             seller_name        = "Music Shop",
                                             wholesale_price    = 10,
                                             retail_price       = 15,
                                             creation_date      = date(2010, 10, 1),
                                             number_of_copies   = 100,
                                             sold_previous_year = 50,
                                             sold_this_year     = 10,
                                             number_of_unsold   = 40, ))

connect.execute(music_records.insert().values(producer_name     = "Motor Music",  
                                             seller_name        = "Music Shop",
                                             wholesale_price    = 21,
                                             retail_price       = 42,
                                             creation_date      = date(2017, 4, 21),
                                             number_of_copies   = 200,
                                             sold_previous_year = 60,
                                             sold_this_year     = 20,
                                             number_of_unsold   = 120, ))

connect.execute(music_records.insert().values(producer_name     = "Nuclear Blast",    
                                             seller_name        = "Nuclear Blast",
                                             wholesale_price    = 12,
                                             retail_price       = 12,
                                             creation_date      = date(2012, 5, 15),
                                             number_of_copies   = 150,
                                             sold_previous_year = 50,
                                             sold_this_year     = 10,
                                             number_of_unsold   = 90, ))

connect.execute(music_records.insert().values(producer_name     = "Stockholm",    
                                             seller_name        = "Stockholm",
                                             wholesale_price    = 5,
                                             retail_price       = 5,
                                             creation_date      = date(2005, 2, 3),
                                             number_of_copies   = 201,
                                             sold_previous_year = 85,
                                             sold_this_year     = 63,
                                             number_of_unsold   = 53, ))
# music records songs
connect.execute(music_records_songs.insert().values(song_id         = connect.execute(songs.select().where(songs.c.name == "Raise Raise")).fetchall()[0][0], 
                                                    music_record_id = connect.execute(music_records.select().where(music_records.c.producer_name == "Motor Music")).fetchall()[0][0]))
connect.execute(music_records_songs.insert().values(song_id         = connect.execute(songs.select().where(songs.c.name == "Zick Zack")).fetchall()[0][0], 
                                                    music_record_id = connect.execute(music_records.select().where(music_records.c.producer_name == "Motor Music")).fetchall()[0][0]))
connect.execute(music_records_songs.insert().values(song_id         = connect.execute(songs.select().where(songs.c.name == "Party in My Head")).fetchall()[0][0], 
                                                    music_record_id = connect.execute(music_records.select().where(music_records.c.producer_name == "Motor Music")).fetchall()[0][0]))

connect.execute(music_records_songs.insert().values(song_id         = connect.execute(songs.select().where(songs.c.name == "Same Old Song")).fetchall()[0][0],
                                                    music_record_id = connect.execute(music_records.select().where(music_records.c.producer_name == "Nuclear Blast")).fetchall()[0][0]))
connect.execute(music_records_songs.insert().values(song_id         = connect.execute(songs.select().where(songs.c.name == "Eisbrecher")).fetchall()[0][0],
                                                    music_record_id = connect.execute(music_records.select().where(music_records.c.producer_name == "Nuclear Blast")).fetchall()[0][0]))

connect.execute(music_records_songs.insert().values(song_id         = connect.execute(songs.select().where(songs.c.name == "Was ist hier los?")).fetchall()[0][0],
                                                    music_record_id = connect.execute(music_records.select().where(music_records.c.producer_name == "Stockholm")).fetchall()[0][0]))
