
import sqlalchemy

YOUR_POSTGRES_PASSWORD = "postgres"
connection_string = f"postgresql://postgres:{YOUR_POSTGRES_PASSWORD}@localhost/postgres"
engine = sqlalchemy.create_engine(
    "postgresql://postgres:postgres@localhost:5432/postgres"
)
db = engine.connect()


def create_tables():
    ## """ create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE IF NOT EXISTS guests (
            name VARCHAR(32) NOT NULL,
            email VARCHAR(50) PRIMARY KEY,
            password VARCHAR(16) NOT NULL,
            credit_card_no VARCHAR(20)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS owners (
            name VARCHAR(32) NOT NULL,
            email VARCHAR(50) PRIMARY KEY,
            password VARCHAR(16) NOT NULL
        );
        """,
        """ 
        CREATE TABLE IF NOT EXISTS properties (
            property_id INTEGER PRIMARY KEY,
            owner VARCHAR(50) NOT NULL,
            property_name VARCHAR(100) NOT NULL,
            property_type VARCHAR(32) NOT NULL,
            price_per_night NUMERIC NOT NULL,
            zipcode NUMERIC(5),
            city VARCHAR(32),
            neighbourhood VARCHAR(32),
            square_feet NUMERIC,
            accomodates INTEGER,
            no_of_bathrooms INTEGER,
            no_of_bedrooms INTEGER,
            amenities VARCHAR(1000),

            FOREIGN KEY (owner) REFERENCES owners (email) ON UPDATE CASCADE ON DELETE CASCADE
            );
        """,
        """
        CREATE TABLE IF NOT EXISTS bookings (
            guest_email VARCHAR(50),
            owner_email VARCHAR(50),
            property_id INTEGER,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            cost NUMERIC,

            FOREIGN KEY (guest_email) REFERENCES guests (email) ON UPDATE CASCADE ON DELETE CASCADE, 
            FOREIGN KEY (owner_email) REFERENCES guests (email) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (property_id) REFERENCES properties (property_id) ON UPDATE CASCADE ON DELETE CASCADE,

            PRIMARY KEY (owner_email, property_id, start_date)
        );
        """,
        """
        CREATE TABLE wishlist (
            guest_email VARCHAR(50),
            property_id INTEGER,

            FOREIGN KEY (guest_email) REFERENCES guests (email) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (property_id) REFERENCES properties (property_id),

            PRIMARY KEY (guest_email, property_id)
        );
        """,
        """
        CREATE TABLE owner_review (
            reviewer_email VARCHAR(50),
            owner_email VARCHAR(50),
            owner_rating NUMERIC(1) CHECK (owner_rating <=5 AND owner_rating >= 0),
            date_reviewed DATE NOT NULL,
            FOREIGN KEY (reviewer_email) REFERENCES guests (email) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (owner_email) REFERENCES owners (email) ON UPDATE CASCADE ON DELETE CASCADE,
            PRIMARY KEY (reviewer_email, owner_email)
        );
        """,
        """
        CREATE TABLE guest_review (
            reviewer_email VARCHAR(50),
            guest_email VARCHAR(50),
            guest_rating NUMERIC(1) CHECK (guest_rating <=5 AND guest_rating >= 0),
            date_reviewed DATE NOT NULL,
            FOREIGN KEY (reviewer_email) REFERENCES owners (email) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (guest_email) REFERENCES guests (email) ON UPDATE CASCADE ON DELETE CASCADE,
            PRIMARY KEY (reviewer_email, guest_email)
        );
        """,
        """
        CREATE TABLE property_review (
            reviewer_email VARCHAR(50),
            property_id INTEGER,
            property_rating NUMERIC(1) CHECK (property_rating <=5 AND property_rating >= 0),
            date_reviewed DATE NOT NULL,
            FOREIGN KEY (reviewer_email) REFERENCES guests (email) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (property_id) REFERENCES properties (property_id) ON UPDATE CASCADE ON DELETE CASCADE,
            PRIMARY KEY (reviewer_email, property_id)
        );
        """
    ]
    for command in commands:
        db.execute(sqlalchemy.text(command))
    return None
    

if __name__ == '__main__':
    create_tables()
