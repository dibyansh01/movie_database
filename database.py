import mysql.connector
import json

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "pandey",
}

# Open the JSON file and load data
with open('imdb.json', 'r') as file:
    data = json.load(file)

# Connect to the MySQL server
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create the 'imdb_movies' database if it doesn't exist
create_db_query = "CREATE DATABASE IF NOT EXISTS imdb_movies;"
cursor.execute(create_db_query)
conn.commit()

# Use the 'imdb_movies' database
db_config["database"] = "imdb_movies"
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create the 'movies' table with the 'genres' column as VARCHAR
create_table_query = """
CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    99popularity FLOAT,
    director VARCHAR(255),
    imdb_score FLOAT,
    name VARCHAR(255),
    genres VARCHAR(255)
);
"""

cursor.execute(create_table_query)

# Insert data into the 'movies' table
for movie in data:
    insert_query = """
    INSERT INTO movies (99popularity, director, imdb_score, name, genres)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (movie["99popularity"], movie["director"], movie["imdb_score"], movie["name"], json.dumps(movie["genre"]))
    cursor.execute(insert_query, values)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created and data populated successfully.")
