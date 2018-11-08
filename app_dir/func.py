from connect import create_connection, close_connection


def list_of_cinemas():
    '''Method returns list with cinemas, each argument is an tuple,
    so user should then take only first index of tuple to get access to
    cinema names'''
    cnx, cursor = create_connection()
    sql = '''
    SELECT name, cinema_id FROM cinemas
    '''
    cursor.execute(sql)
    cinemas = cursor.fetchall()
    close_connection(cnx, cursor)
    return cinemas


def list_of_movies():
    '''This method returns a dictionary where cinema_id is a key and its values are
    id of movies played in this cinema.
    '''

    cinemas = list_of_cinemas()
    c_id = []
    movie_cinema_dict = {}
    for cinema in cinemas:
        c_id.append(cinema[1])
    cnx, cursor = create_connection()

    for index in c_id:
        sql = '''
        SELECT movie_id FROM movies
        WHERE cinema_id = %s
        '''
        cursor.execute(sql, (index, ))
        result = cursor.fetchall()

        movies = [r[0] for r in result]
        movie_cinema_dict[index] = movies

    return movie_cinema_dict


def movie_info(movie_id):
    '''This function returns a list with informations of movie
    returned tuple look like this:
    ('It', Decimal('7.1'), Decimal('12.99'), 100, datetime.timedelta(0, 70800), 13, 95, 1)'''
    cnx, cursor = create_connection()
    sql = '''
    SELECT name, rating, price, seats, date_trunc('minute', hour), approved_age,
     seats_left, cinema_id FROM movies
    WHERE movie_id = %s
    '''
    cursor.execute(sql, (movie_id, ))
    result = cursor.fetchone()
    close_connection(cnx, cursor)
    return result


def all_movies():
    '''This function returns a dictionary with
    name of the movie as a key and list of 2 values
    first - list of cinemas where the movie is played
    second - an avarage rating of this movie
    output of this function looks like this:
    {'Split': [['DCF'], Decimal('8.1')], 'It': [['DCF', 'Korona'], Decimal('7.15')]}'''

    cnx, cursor = create_connection()
    sql = '''
    SELECT movie_id, cinemas.name, movies.name, rating, approved_age
    FROM movies JOIN cinemas ON
    cinemas.cinema_id = movies.cinema_id
    '''
    cursor.execute(sql)
    list_of_movies = cursor.fetchall()
    overall = {}
    for m in list_of_movies:
        if m[2] in overall:
            before_rating = overall[m[2]][1]
            overall[m[2]][0].append(m[1])
            overall[m[2]][1] = (before_rating + m[3]) / 2
        else:
            overall[m[2]] = [[m[1]], m[3], m[4]]
    return overall

    close_connection(cnx, cursor)
    return list_of_movies


def cinema_stats():
    '''This method returns a dictionary where cinema_id is a key and values are 
    informations about this cinema like, total amount of selled tickets,
    average tickets per movie, percentege value of average, total income'''
    cinemas_id = [el[1] for el in list_of_cinemas()]
    cnx, cursor = create_connection()

    tickets = {}

    for id in cinemas_id:
        sql = '''
        SELECT payment_id, movie_id, price FROM
        payments WHERE cinema_id = %s
        '''
        cursor.execute(sql, (id, ))
        matches = cursor.fetchall()
        sum_of_price = sum([el[2] for el in matches])
        all_payments = len(matches)

        sql = '''
        SELECT seats FROM movies
        WHERE cinema_id = %s
        '''
        cursor.execute(sql, (id, ))

        match = cursor.fetchall()
        if match != []:
            seats = sum([el[0] for el in match])

            tickets_per_movie = all_payments / len(match)

            averrage = all_payments / seats
            percentage_value = "{:.2f}%".format(averrage * 100)
        else:
            all_payments = 0
            tickets_per_movie = 0
            percentage_value = "0.00%"
            sum_of_price = 0
        tickets[id] = [all_payments, tickets_per_movie,
                       percentage_value, sum_of_price]

    close_connection(cnx, cursor)
    return tickets


def create_user(name, surname, age):
    '''This method creates new user in users database,
    to create user function needs parameters like: 
    name, surname, age.'''
    cnx, cursor = create_connection()
    sql = '''
    INSERT INTO users (name, surname, age, balance)
    values (%s, %s, %s, %s)
    RETURNING user_id
    '''
    cursor.execute(sql, (name, surname, age, 1000))
    user_id = cursor.fetchone()[0]
    close_connection(cnx, cursor)
    return user_id


def buy_ticket(name, surname, age, price, movie_id, cinema_id, approved_age):
    """This method takes care about buying ticket transaction. 
    Method adds new payment to payments table in database, and creates new user 
    if doesn't exist. Also this method takes care about changing a balance of a user"""
    cnx, cursor = create_connection()
    sql = '''
    SELECT user_id FROM users
    WHERE name = %s AND surname = %s AND age = %s
    '''
    cursor.execute(sql, (name, surname, age))
    result = cursor.fetchone()
    if result == None:
        user_id = create_user(name, surname, age)
    else:
        user_id = result[0]

    sql = '''INSERT INTO payments (user_id, movie_id, cinema_id, price)
            VALUES (%s, %s, %s, %s)'''
    cursor.execute(sql, (user_id, movie_id, cinema_id, price))

    sql = ''' UPDATE movies SET seats_left = seats_left - 1
        WHERE movie_id = %s
        '''
    cursor.execute(sql, (movie_id,))

    sql = '''
    UPDATE users SET balance = balance - %s
    WHERE user_id = %s
    '''
    cursor.execute(sql, (price, user_id))

    close_connection(cnx, cursor)


def create_movie(cinema_name, name, rating, price, seats, hour, approved_age):
    '''This method creates a new movie. To successfully add a new movie, we need to 
    have some crucial informations like cinema_name or movie name etc.'''
    cnx, cursor = create_connection()
    sql = '''
    SELECT cinema_id FROM cinemas WHERE name = %s
    '''
    cursor.execute(sql, (cinema_name,))
    cinema_id = cursor.fetchone()[0]
    sql = '''
    INSERT INTO movies (cinema_id, name, rating, price, seats, hour, approved_age, seats_left)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(sql, (cinema_id, name, rating, price,
                         seats, hour, approved_age, seats))

    close_connection(cnx, cursor)
