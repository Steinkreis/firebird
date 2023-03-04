from sqlalchemy import create_engine
import sqlalchemy.engine.base
from furl import furl
from pathlib import Path

def connection(db_path: str, client_path: str) -> sqlalchemy.engine.base.Engine:
    username = 'SYSDBA'
    password = 'masterkey'
    hostname = 'localhost'
    db_path = db_path.replace('\\', '/')

    client_path = Path(client_path)
    url = furl(scheme='firebird', username=username, password=password, host=hostname, path=db_path)
    engine = create_engine(
        str(url),
        connect_args={"fb_library_name": str(client_path)}
    )
    return engine

