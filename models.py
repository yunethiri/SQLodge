import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask_login import UserMixin


YOUR_POSTGRES_PASSWORD = "postgres"
connection_string = f"postgresql://postgres:{YOUR_POSTGRES_PASSWORD}@localhost/postgres"
engine = sqlalchemy.create_engine(
    "postgresql://postgres:postgres@localhost/postgres"
)

db = engine.connect()

session = Session(engine)

class NewUserMixin(UserMixin):
    def get_id(self):
        return self.email
    
Base = automap_base(cls=NewUserMixin)
Base.prepare(autoload_with=engine)


Guests = Base.classes.guests
Owners = Base.classes.owners    
Properties = Base.classes.properties
Bookings = Base.classes.bookings