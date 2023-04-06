import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask_login import UserMixin


YOUR_POSTGRES_PASSWORD = "postgres"
port = 5432
connection_string = f"postgresql://postgres:{YOUR_POSTGRES_PASSWORD}@localhost:{port}/postgres"
engine = sqlalchemy.create_engine(
    f"postgresql://postgres:postgres@localhost:{port}/postgres"
)

db = engine.connect()

session = Session(engine)

class NewUserMixin(UserMixin):
    def get_id(self):
        return self.email
    
Base = automap_base(cls=NewUserMixin)
Base.prepare(autoload_with=engine)

Users = Base.classes.users    
Properties = Base.classes.properties
Bookings = Base.classes.bookings