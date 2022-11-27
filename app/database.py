from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#sqlalchemy_db_url = 'postgresql://postgres:sysadmin@localhost/fastapi'
#SQLALCHEMY_DB_URL = f'postgresql://{Settings.database_username}:{Settings.database_password}@{Settings.database_hostname}:{Settings.database_port}/{Settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='sysadmin', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print ("database connection is successfull")
        break
    except Exception as error:
        print(f"database connection failed {error}")
        time.sleep(10)
"""