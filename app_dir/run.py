from flask import Flask, render_template, url_for, redirect, request
from connect import create_connection, close_connection
from func import list_of_cinemas, list_of_movies, movie_info, all_movies, cinema_stats, buy_ticket, create_movie
from reports import generate_xls, generate_pdf


app = Flask(__name__)


@app.route('/', methods=('GET',))
@app.route('/home', methods=('GET',))
def home():
    if request.method == 'GET':
        return render_template('home.html')


@app.route('/movies', methods=('GET', 'POST'))
def movies():
    if request.method == 'GET':
        dict_of_movies = all_movies()
        return render_template('movies.html', dict_of_movies=dict_of_movies)


@app.route('/cinemas', methods=('GET', 'POST'))
def cinemas():
    if request.method == 'GET':
        cinemas_list = list_of_cinemas()
        movies_list = list_of_movies()
        return render_template('cinemas.html', cinemas=cinemas_list, movies_list=movies_list, movie_info=movie_info)
    else:
        pass


@app.route('/stats', methods=('GET', 'POST'))
def stats():
    if request.method == 'GET':
        info = cinema_stats()
        cinemas = list_of_cinemas()
        return render_template('stats.html', tickets=info, cinemas=cinemas)
    else:
        if request.form['btn'] == "xls":
            generate_xls()
            return "Generated XLS file " + "<a href='{}'>Home page</a>".format(url_for('home'))
        elif request.form['btn'] == 'pdf':
            generate_pdf()
            return "Generated pdf file" + "<a href='{}'>Home page</a>".format(url_for('home'))


@app.route('/add/<movie_id>', methods=('GET', 'POST'))
def add_movie(movie_id):
    info = movie_info(movie_id)
    if request.method == 'GET':
        return render_template('add.html', info=info)
    else:
        username = request.form['name']
        surname = request.form['surname']
        age = request.form['age']

        if int(age) < info[5]:
            return "You're too young to this movie. We're sorry! (Honestly - we just wanted your money)" + "<a href='{}'>Home page</a>".format(url_for('home'))

        buy_ticket(username, surname, int(age),
                   info[2], movie_id, info[7], info[5])
        return "Ticket has been succesfully bought!" + "<a href='{}'>Home page</a>".format(url_for('home'))


@app.route('/new_movie', methods=('GET', 'POST'))
def new_movie():
    if request.method == 'GET':
        cinemas = list_of_cinemas()
        return render_template('new_movie.html', cinemas=cinemas)
    else:
        name = request.form['name']
        rating = request.form['rating']
        price = request.form['price']
        seats = request.form['seats']
        time = request.form['hour']
        approved_age = request.form['approved_age']
        cinema_name = request.form['cinema_id']

        create_movie(cinema_name, name, float(rating),
                     float(price), int(seats), time, int(approved_age))
        return "New movie was succesfully created ! " + "<a href='{}'>Home page</a>".format(url_for('home'))


if __name__ == '__main__':
    app.run()
