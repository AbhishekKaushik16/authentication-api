def get_db_session(env):
    from api.base.client import Client
    from api.utils.logger import logger

    logger.info("Setting up Client")
    client = Client(env)
    session = client.session_factory()
    logger.info("Setting Schema and Lookup Schema")
    client._set_schema(session)
    return session
