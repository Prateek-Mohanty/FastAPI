from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import configparser

config = configparser.ConfigParser()

config.read('config.ini')

sqlite_url = config['database']['sqlite_database_url']
postgres_url = config['database']['postgresql_database_url']
mysql_url = config['database']['mysql_database_url']


DATABASE_URL = sqlite_url

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})
