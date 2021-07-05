from sqlalchemy import Column, MetaData
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql.sqltypes import Text

base_object = declarative_base(metadata=MetaData())


class userMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__tablename__.lower()

    id = Column(Text, primary_key=True)
