# initial database creation
from numbers import Integral
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData

engine = create_engine('sqlite:///music_shop.db', echo = False)
meta = MetaData()

# basic tables for database
musicians = Table(
   'musicians', meta, 
   Column('musician_id', Integer, primary_key = True), 
   Column('first_name', String), 
   Column('last_name', String), 
   Column('band_id', Integer, ForeignKey('bands.band_id')), 
   Column('role', String), 
)

bands = Table(
   'bands', meta, 
   Column('band_id', Integer, primary_key = True), 
   Column('name', String), 
)

songs = Table(
   'songs', meta, 
   Column('song_id', Integer, primary_key = True), 
   Column('band_id', Integer, ForeignKey('bands.band_id')), 
   Column('name', String), 
)

music_records = Table(
   'music_records', meta, 
   Column('music_record_id', Integer, primary_key = True), 
   Column('producer_name', String), 
   # Column('seller_name', String), 
   # Column('wholesale_price', Integer),
   # Column('retail_price', Integer), 
   # Column('creation_date', Integer),
   # Column('number_of_copies', Integer), 
   # Column('sold_previous_year', Integer), 
   # Column('sold_this_year', Integer),
   # Column('number_of_unsold', Integer),
)

music_records_songs = Table(
   'music_records_songs', meta, 
   Column('song_id', Integer, ForeignKey('songs.song_id')),
   Column('music_record_id', Integer, ForeignKey('music_record.music_record_id')),
)

# connect to database and create all tables
connect = engine.connect()
meta.create_all(engine)

# insert sampels 
insert_mus_1 = musicians.insert().values(first_name = 'Till', last_name = 'Lindemann', role = 'Vocal',  band_name = 'rammstein')
insert_mus_2 = musicians.insert().values(first_name = 'Paul', last_name = 'Landers',   role = 'Guitar', band_name = 'rammstein')

insert_mus_3 = musicians.insert().values(first_name = 'Peter', last_name = 'Tägtgren', role = 'Мocal', band_name = 'Pain')

insert_mus_4 = musicians.insert().values(first_name = 'Alexander', last_name = 'Wesselsky', role = 'Vocal', band_name = 'Eisbrecher')

connect.execute(insert_mus_1)
connect.execute(insert_mus_2)
connect.execute(insert_mus_3)
connect.execute(insert_mus_4)
