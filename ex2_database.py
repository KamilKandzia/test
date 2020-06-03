#for anaconda env dll should be downloaded https://stackoverflow.com/questions/54876404/unable-to-import-sqlite3-using-anaconda-python
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///C:\\Users\\Kamil\\Desktop\\test\\database.db', echo=True)
Base = declarative_base()

class Table(Base):

    __tablename__ = "todolist"

    id = Column(String, primary_key=True)
    name = Column(String)
    deadline = Column(Integer)
    description = Column(String)


    def __init__(self, name):
        self.name = name    

Table.metadata.create_all(engine)