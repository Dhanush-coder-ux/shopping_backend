from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

    
#postgresql://neondb_owner:npg_pHa5zGtFrAW0@ep-long-mouse-a1r0owaz-pooler.ap-southeast-1.aws.neon.tech/neondb
DATABASE_URL ="postgresql://neondb_owner:npg_pHa5zGtFrAW0@ep-long-mouse-a1r0owaz-pooler.ap-southeast-1.aws.neon.tech/neondb"
engine = create_engine(DATABASE_URL,echo=True)
SessionLocal = sessionmaker(autoflush=False,autocommit = False,bind=engine)
Base = declarative_base()