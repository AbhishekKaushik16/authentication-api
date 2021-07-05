from api.utils.helpers import get_all_attr, get_class_by_tablename
import logging

from api.utils.db_connection import get_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .utils.utils import update_object_from_dict
from ..utils.logger import logger


class Client:
    def __init__(self, config):
        # self.config = self.process_config(config)
        self.config = config
        self.logger = logger
        logger.info("Creating SQL Alchemy Engine")
        engine = get_engine(config["database"])
        logger.info("Creating SQL Alchemy scoped sessions")
        self.session_factory = scoped_session(sessionmaker(bind=engine))
        if config.get("debug", "false").lower() == "true":
            logger.setLevel(logging.DEBUG)
        self.logger.info(
            "Database Configuration...",
            extra={"meta": {"Database Configuration": config}},
        )

    def _set_schema(self, session):
        schema_str = "SET SEARCH_PATH TO " + self.config["database"]["schema"]
        self.logger.info("Database Schema: {}".format(schema_str))
        session.execute(schema_str)

    def search_by_id(self, resource, _id):
        session = self.session_factory()
        self._set_schema(session)

        table_obj = get_class_by_tablename(resource)
        search_result = session.query(table_obj).get(_id)
        search_result = get_all_attr(search_result)
        return search_result

    def insert_data(self, resource, data):
        try:
            session = self.session_factory()
            self._set_schema(session)

            table_obj = get_class_by_tablename(resource)
            obj = table_obj(data)
            session.add(obj)
            session.commit()
            return True
        except Exception as exc:
            print(exc)
            return False

    def update_data(self, resource: str, data: dict):
        try:
            session = self.session_factory()
            self._set_schema(session)

            table_obj = get_class_by_tablename(resource)
            search_result = session.query(table_obj).filter_by(id=data.get('id')).first()
            update_object_from_dict(search_result, data)
            session.commit()
            return True
        except Exception as exc:
            print(exc)
            session.rollback()
            return False
