from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

DATABASE_URL = "mysql+mysqlconnector://admin:Root*1234@localhost:3306/flaskdb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    password = Column(String(200))

    # Establish a one-to-many relationship with orders
    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    quantity = Column(Integer, index=True)

    # Establish a foreign key relationship with users
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")


# Create database tables


Base.metadata.create_all(bind=engine)
