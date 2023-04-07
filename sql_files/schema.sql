CREATE TABLE IF NOT EXISTS users (
    name VARCHAR(32) NOT NULL,
    email VARCHAR(50) PRIMARY KEY,
    password VARCHAR(16) NOT NULL
);

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

    FOREIGN KEY (owner) REFERENCES users (email) ON UPDATE CASCADE ON DELETE CASCADE
    );

CREATE TABLE IF NOT EXISTS bookings (
    guest_email VARCHAR(50),
    owner_email VARCHAR(50),
    property_id INTEGER,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    duration NUMERIC,

    FOREIGN KEY (guest_email) REFERENCES users (email) ON UPDATE CASCADE ON DELETE CASCADE, 
    FOREIGN KEY (owner_email) REFERENCES users (email) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties (property_id) ON UPDATE CASCADE ON DELETE CASCADE,

    PRIMARY KEY (property_id, start_date),
    CHECK (guest_email != owner_email), 
    CHECK (start_date < end_date)
);