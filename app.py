from flask import Flask, render_template, request, abort, jsonify
from helpers import getNetflixMovies
from database import get_db_connection  # Imports your PostgreSQL handshake

app = Flask(__name__)

# --- EXISTING ROUTES ---

@app.route("/")
def home():
    return render_template("Home.html")


@app.route("/welcome", methods=["GET"])
def welcome():
    return render_template("Welcome.html")


@app.route("/movies/<name>", methods=["GET"])
def movies(name):
    if name == "Nidhi":
        # Your helper call for Nidhi:
        movie_list = getNetflixMovies(name)
        return f"Hello, {name}! Recommended: {', '.join(movie_list)}"

    elif name == "Alice":
        return (
            f"Hello, {name}! Here are some movies you might like: Harry Potter, Narnia."
        )
    else:
        abort(404)


# --- DATABASE ROUTES (GET & POST) ---

@app.route("/GETPOST", methods=["GET"])
def view_ratings():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        # Fetch the data
        cur.execute("SELECT movie_name, feedback FROM movie_ratings;")
        rows = cur.fetchall() # This is a list of your movies
        cur.close()
        conn.close()
        
       
        return render_template("GETPOST.html", ratings=rows)
    
    return "Database connection failed", 500


# POST: Add a new rating to your Postgres table
@app.route("/add-rating", methods=["POST"])
def add_rating():
    # This checks if the data came from an HTML Form or a JSON API (Postman)
    if request.is_json:
        data = request.get_json()
        movie_name = data.get('movie_name')
        feedback = data.get('feedback')
    else:
        movie_name = request.form.get('movie_name')
        feedback = request.form.get('feedback')

    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO movie_ratings (movie_name, feedback) VALUES (%s, %s)",
            (movie_name, feedback)
        )
        conn.commit()
        cur.close()
        conn.close()
        return f"Successfully added {movie_name}! Go back to check /GETPOST for all ratings."
    
    return "Database connection failed", 500


if __name__ == "__main__":
    app.run(debug=True)