from flask import Flask, request, jsonify
import mysql.connector
import json

app = Flask(__name__)

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "pandey",
    "database": "imdb_movies",
}

# Connecting to the MySQL server
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


# API routes
@app.route('/movies', methods=['GET'])
def get_movies():
    # Fetching all movies from the 'movies' table
    cursor.execute("SELECT * FROM movies")
    movies = []
    for row in cursor.fetchall():
        movie = {
            "id": row[0],
            "99popularity": float(row[1]),
            "director": row[2],
            "imdb_score": float(row[3]),
            "name": row[4],
            "genres": json.loads(row[5]) if row[5] else []      # Loading genres as a list
        }
        movies.append(movie)

    return jsonify(movies)


@app.route('/movies/search', methods=['GET'])
def search_movies():
    criteria = {}
    name = request.args.get('name')
    if name:
        criteria['name'] = '%' + name + '%'

    director = request.args.get('director')
    if director:
        criteria['director'] = '%' + director + '%'

    genre = request.args.get('genre')
    if genre:
        criteria['genres'] = '%' + genre + '%'

    imdb_score = request.args.get('imdb_score')
    if imdb_score:
        criteria['imdb_score'] = float(imdb_score)

    # Building the SQL query dynamically based on the provided criteria
    query = "SELECT * FROM movies WHERE "
    conditions = []
    values = ()

    for key, value in criteria.items():
        conditions.append(f"{key} LIKE %s")
        values += (value,)

    if conditions:
        query += " AND ".join(conditions)
        cursor.execute(query, values)
    else:
        # if No search criteria provided, return all movies
        cursor.execute("SELECT * FROM movies")

    movies = []
    for row in cursor.fetchall():
        movie = {
            "id": row[0],
            "99popularity": float(row[1]),
            "director": row[2],
            "imdb_score": float(row[3]),
            "name": row[4],
            "genres": json.loads(row[5]) if row[5] else []
        }
        movies.append(movie)

    return jsonify(movies)


@app.route('/admin/movies', methods=['POST'])
def add_movie():
    # Checking if the request has a JSON body
    if not request.json:
        return jsonify({"error": "Data is missing or not in JSON format"}), 400

    new_movie = request.json
    try:
        # Inserting the new movie into the 'movies' table
        insert_query = """
        INSERT INTO movies (99popularity, director, imdb_score, name, genres)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            float(new_movie["99popularity"]),
            new_movie["director"],
            float(new_movie["imdb_score"]),
            new_movie["name"],
            json.dumps(new_movie["genre"]),
        )
        cursor.execute(insert_query, values)
        conn.commit()

        # Fetching the inserted movie with its assigned ID
        cursor.execute("SELECT * FROM movies WHERE id = LAST_INSERT_ID()")
        inserted_movie = cursor.fetchone()

        if inserted_movie:
            movie = {
                "id": inserted_movie[0],
                "99popularity": float(inserted_movie[1]),
                "director": inserted_movie[2],
                "imdb_score": float(inserted_movie[3]),
                "name": inserted_movie[4],
                "genre": json.loads(inserted_movie[5]) if inserted_movie[5] else [],  # Use "genre" without 's'
            }
            return jsonify({"message": "Movie added successfully", "movie": movie}), 201
        else:
            return jsonify({"error": "Failed to fetch the inserted movie"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Admin route for editing an existing movie
@app.route('/admin/movies/<int:movie_id>', methods=['PUT'])
def edit_movie(movie_id):
    # Check if the request has a JSON body
    if not request.json:
        return jsonify({"error": "Data is missing or not in JSON format"}), 400

    # Checking if the movie exists
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    existing_movie = cursor.fetchone()
    if not existing_movie:
        return jsonify({"error": "Movie not found"}), 404

    try:
        updated_data = request.json

        # Updating the movie in the 'movies' table
        update_query = """
        UPDATE movies
        SET 99popularity = %s, director = %s, imdb_score = %s, name = %s, genres = %s
        WHERE id = %s
        """
        values = (
            float(updated_data["99popularity"]),
            updated_data["director"],
            float(updated_data["imdb_score"]),
            updated_data["name"],
            json.dumps(updated_data["genre"]),
            movie_id,
        )
        cursor.execute(update_query, values)
        conn.commit()

        # Fetching the updated movie
        cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
        updated_movie = cursor.fetchone()

        if updated_movie:
            movie = {
                "id": updated_movie[0],
                "99popularity": float(updated_movie[1]),
                "director": updated_movie[2],
                "imdb_score": float(updated_movie[3]),
                "name": updated_movie[4],
                "genre": json.loads(updated_movie[5]) if updated_movie[5] else [],
            }
            return jsonify({"message": "Movie updated successfully", "movie": movie})
        else:
            return jsonify({"error": "Failed to fetch the updated movie"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Admin route for deleting a movie
@app.route('/admin/movies/<int:movie_id>', methods=['DELETE'])
def remove_movie(movie_id):
    # Check if the movie exists
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    existing_movie = cursor.fetchone()
    if not existing_movie:
        return jsonify({"error": "Movie not found"}), 404

    try:
        # Deleting the movie from the 'movies' table
        delete_query = "DELETE FROM movies WHERE id = %s"
        cursor.execute(delete_query, (movie_id,))
        conn.commit()

        return jsonify({"message": "Movie removed successfully", "movie": existing_movie})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
