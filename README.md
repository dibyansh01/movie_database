# Movie Database

## Overview

The Movie Database API is a RESTful web service that allows users to access and search movie based on different criteria. It is built using the Flask framework and uses MySQL as the underlying database for data storage. The API provides access to movie information, search functionality, and CRUD (Create, Read, Update, Delete) operations for administrators.

## Base URL

The base URL for accessing the API is `http://127.0.0.1:5000` when running the API locally. Ensure the API is running to access its endpoints.

## Authentication

The API currently does not implement authentication or authorization. It offers two access levels:

1. **Admin**: Users with admin privileges can perform CRUD operations on movie entries.
2. **Users**: Regular users can view movie listings and use the search functionality.

## Endpoints

### 1. Retrieve Movies

**GET /movies**

- Description: Retrieve a list of all movies.
- Response:
  - Status Code: 200 OK
  - Content: List of movie objects, each containing:
    - `id`: Unique identifier for the movie.
    - `99popularity`: Popularity score of the movie (float).
    - `director`: Director of the movie.
    - `imdb_score`: IMDb rating of the movie (float).
    - `name`: Name of the movie.
    - `genres`: List of genres associated with the movie (array).

### 2. Search Movies

**GET /movies/search**

- Description: Search for movies based on various criteria, including 'name,' 'director,' 'genre,' and 'imdb_score.'
- Query Parameters:
  - `name` (optional): Movie name or part of the name to search for.
  - `director` (optional): Director's name or part of the name to search for.
  - `genre` (optional): Genre or part of the genre to search for.
  - `imdb_score` (optional): IMDb score to filter movies by.
- Response:
  - Status Code: 200 OK
  - Content: List of movie objects (filtered by search criteria), each containing the same attributes as in the "Retrieve Movies" endpoint.

### 3. Add Movie (Admin Only)

**POST /admin/movies**

- Description: Add a new movie to the database.
- Request Body: JSON object with movie details, including:
  - `99popularity`: Popularity score of the movie (float).
  - `director`: Director of the movie.
  - `imdb_score`: IMDb rating of the movie (float).
  - `name`: Name of the movie.
  - `genre`: List of genres associated with the movie (array).
- Response:
  - Status Code: 201 Created
  - Content: JSON object with a success message and the added movie details.

### 4. Edit Movie (Admin Only)

**PUT /admin/movies/{movie_id}**

- Description: Edit an existing movie in the database.
- Request Body: JSON object with updated movie details (similar structure to the "Add Movie" request).
- Path Parameter:
  - `movie_id`: Unique identifier of the movie to be edited.
- Response:
  - Status Code: 200 OK
  - Content: JSON object with a success message and the updated movie details.

### 5. Remove Movie (Admin Only)

**DELETE /admin/movies/{movie_id}**

- Description: Remove a movie from the database.
- Path Parameter:
  - `movie_id`: Unique identifier of the movie to be removed.
- Response:
  - Status Code: 200 OK
  - Content: JSON object with a success message and the removed movie details.

## Usage

Here are some example API requests:

- Retrieve all movies:
  - Request: GET `/movies`

- Search for movies by name:
  - Request: GET `/movies/search?name=Star Wars`

- Add a new movie (admin only):
  - Request: POST `/admin/movies`
  - Request Body:
    ```json
    {
        "99popularity": 88.0,
        "director": "George Lucas",
        "imdb_score": 8.8,
        "name": "Star Wars",
        "genre": ["Action", "Adventure", "Fantasy", "Sci-Fi"]
    }
    ```

- Edit an existing movie (admin only):
  - Request: PUT `/admin/movies/1`
  - Request Body:
    ```json
    {
        "99popularity": 85.0,
        "director": "Updated Director",
        "imdb_score": 9.0,
        "name": "Updated Movie",
        "genre": ["Action", "Adventure"]
    }
    ```

- Remove a movie (admin only):
  - Request: DELETE `/admin/movies/1`

## Error Handling

The API provides error messages in JSON format for various scenarios, such as missing data, movie not found, or internal server errors. Users should check the response status code and content for error details.

## Running Locally

To run the API locally, follow these steps:

1. Ensure you have Python, Flask, and MySQL installed.
2. You can use requirements.txt file to recreate the environment on your system using the pip install -r command: `pip install -r requirements.txt`
3. The first step is to configure the MySQL database connection in the `database.py` file and run the `database.py` script for populating your local database with imdb.json.
4. In the second step, configure the `db_config` in main.py and then run the `main.py` script to start the Flask development server.

## Additional Features

In order to increase security and scalability, I'm working to improve the application by integrating new features like user authentication, user roles, rate limiting, and pagination.


