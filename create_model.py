from MainServer.tables import base
from MainServer.database import engine


base.metadata.create_all(engine)