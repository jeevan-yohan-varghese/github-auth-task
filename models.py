from sqlalchemy import Column,DateTime,ForeignKey,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base=declarative_base()


class Repo(Base):
    __tablename__="repo"
    repo_id=Column(String,primary_key=True)
    repo_name=Column(String,primary_key=True)
    owner_id=Column(String)
    owner_name=Column(String)
    owner_email=Column(String)
    status=Column(String)
    stars=Column(Integer)


    

