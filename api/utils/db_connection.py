from sqlalchemy import create_engine


def get_engine(config):
    conn_str = "postgresql://{user}:{password}@{host}:{port}/{dbname}".format(
        user=config.get("user"),
        host=config.get("host"),
        port=int(config.get("port")),
        password=config.get("password"),
        dbname=config.get("dbname"),
    )
    return create_engine(conn_str, pool_size=100, max_overflow=100, pool_pre_ping=False)
