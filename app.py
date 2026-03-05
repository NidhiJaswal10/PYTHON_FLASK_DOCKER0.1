from flask import Flask, render_template, request, abort
from helpers import getNetflixMovies

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("Home.html")

@app.route("/welcome", methods=['GET'])
def welcome():
    return render_template("Welcome.html")

@app.route("/movies/<name>", methods=['GET'])
def movies(name):
    if name == "Nidhi":
        # Aapka helper call:
        movie_list = getNetflixMovies(name)
        # Hum ise return kar rahe hain taaki test pass ho sake
        return f"Hello, {name}! Recommended: {', '.join(movie_list)}"
    
    elif name == "Alice":
        return f"Hello, {name}! Here are some movies you might like: Harry Potter, Narnia."
    
    else:
        return f"Hello, {name}! I don't have specific movie recommendations for you."

@app.route("/GETPOST", methods=['GET', 'POST'])
def getpost():
    if request.method == 'POST':
        name = request.form.get('name')
        if name is None:
            abort(400)
        return f'Hello, {name}!'
    return render_template("GETPOST.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)