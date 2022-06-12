# file to load data from sqlite file and provide some interfaces 

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData

# connect to existing database
engine = create_engine('sqlite:///music_shop.db', echo = False)
meta = MetaData(engine)

# load data from tables
musicians = Table("musicians", meta, autoload = True)
bands     = Table("bands",     meta, autoload = True)
songs     = Table("songs",     meta, autoload = True)
music_records = Table("music_records", meta, autoload = True)

# функция позволяющая получить количество музыкальных произведений заданного ансамбля

# функция позволяющая выводить название всех компакт-дисков заданного ансамбля

# функция позволяющая показать лидеров продаж текущего года, то есть названия
# компакт-дисков, которые чаще всего покупали в текущем
# году

# функция позволяющая вносить изменения данных о компакт-дисках и ввод
# новых данных

# функция позволяющая предусмотреть вводить новые данных об ансамблях 
# (добавлять новые ансамбли можно и так через обычный insert)