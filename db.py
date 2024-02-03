from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey


DATABASE_URL = "mysql+mysqlconnector://root:12345@localhost:3306/flask"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    password = Column(String(200))

class order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)    
    
# Create database tables
Base.metadata.create_all(bind=engine)