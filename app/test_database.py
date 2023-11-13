from databases import Database
import os
import sqlalchemy
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = 'postgresql://' + os.getenv("DATABASE_USER") + ':' + os.getenv("DATABASE_PASSWORD") + '@' + os.getenv("DATABASE_HOST") + '/' + os.getenv("DATABASE_TEST")
database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


