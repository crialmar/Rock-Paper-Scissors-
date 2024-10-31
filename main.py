'''Imports'''
import sqlite3
import random

# TODO -----> | EXTRAER LOS DATOS NECESARIOS | AÑADIR DATOS A TABLA | INYECCION DATOS |
# TODO -----> win/ fail no se hace bien la cuenta si se repire varias veces, n_match sí


def create_db():
    '''Creation of db'''
    conn = sqlite3.connect("rps.db")
    conn.commit()
    conn.close()


def create_table_user():
    '''Creation of match database user'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user text NOT NULL UNIQUE,
            email text NOT NULL UNIQUE,
            n_match integer,
            win integer,
            fail integer
        )"""
    )
    conn.commit()
    conn.close()


def create_table_match():
    '''Creation of match database table'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE match (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id integer,
            rounds integer,
            results text,
            move text,
            date DATE DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user(id)
        )"""
    )
    conn.commit()
    conn.close()


def create_table_round():
    '''Creation of round database table'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE round (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id integer,
            results text, 
            move text,
            date DATE DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(match_id) REFERENCES match(id)
        )"""
    )
    conn.commit()
    conn.close()


def start_match():
    '''Start of the game'''
    #? 1. INTRODUCCIÓN AL JUEGO
    print("\n******* Rock Paper Scissors *******\n")
    user = input("Hi! What's your name? ").lower() 
    email = input("Please, tell us your email: ")
    return user, email


def match():
    '''Logic for one match (3 rounds)'''
    #? 2. ELECCIÓN DEL USUARIO
    print("\nGreat! You'll be playing against the machine")
    options = ['R', 'P', 'S'] #* Establecemos las opciones que tiene la máquina
    round_results = []
    score = 0
   
    round = 0
    for _ in range (3):
        print(f'***** FIGHT *****\n')
        while True:
            try:
                move = input("Please choose an option: Rock (R), Paper (P) or Scissors (S) ").upper()
                options.index(move)
            except ValueError:
                print("That is not an option. Try again")
            else:
                break
        #? 3. ELECCIÓN DE LA MÁQUINA
        computer_choice = random.choice(options) #*Randomizamos la elección de la máquina
        #? 4. EL COMBATE
        if move == computer_choice:
            print(f'{move} vs {computer_choice}. In case of a tie, the machine wins\n')
            result = 'Fail '
        elif (move == 'R' and computer_choice == 'S') or \
            (move == 'S' and computer_choice == 'P') or \
            (move == 'P' and computer_choice == 'R'):
            print(f'{move} vs {computer_choice}. You win\n')
            result = 'Win '
            score += 1
        else:
            print(f'{move} vs {computer_choice}. Machine wins\n')
            result = 'Fail '
        round_results.append(result)
        round += 1
    print("\n******* RESULTS *******\n")
    print(f'The results are {round_results}. Your score is {score}')
    win = 0
    fail = 0
    if score >= 2:
        win += 1
        print("You won the game!!!\n")
    else:
        fail += 1
        print("The machine has won\n")
    return win, fail, round, move


def end_match():
    '''Logic for the end of the game, deciding whether to play another game or not'''
    n_match = 0
    while True:
        try:
            other_match = input('Do want to play again? Yes (Y) or No (N): ').upper()
            ['Y', 'N'].index(other_match)
            if other_match == 'Y':
                # total_round = round + {round}
                n_match += 1
                match()
        except ValueError:
            print("That is not an option. Try again")
        else:
            if other_match == 'N':
                n_match += 1
                print('Thanks')
                break
    return n_match


def data_users_mail(user, email):
    '''Insert user and email data to db users table'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
                       INSERT INTO users (user, email) 
                       VALUES (?, ?) 
                       ''', (user, email))
        conn.commit()
        print('User and email register correctly')
    except sqlite3.IntegrityError:
        print (f'Hi {user}')
    finally:
        conn.close()


def data_users_game(n_match, win, fail, user):
    '''Insert n_match, win and fail data to db users table'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
                      UPDATE users
                      SET 
                        n_match = n_match + ?, 
                        win = win + ?, 
                        fail = fail + ?
                      WHERE user = ?
                      ''', (n_match, win, fail, user))
        conn.commit()
        print('Data saved correctly')
    except sqlite3.IntegrityError:
        print ('There was an error saving the data')
    finally:
        conn.close()


def data_match(round, move, user):
    '''Insert data to db match table---> user_id, rounds, results, move'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE user = ?", (user,))
        user_id_result = cursor.fetchone()
        if user_id_result is None:
            print("User not found")
            return
        user_id = user_id_result[0]
        cursor.execute('''
                       INSERT INTO match (user_id, rounds, move) 
                       VALUES (?, ?, ?) 
                       ''', (user_id, round,  move))
        conn.commit()
        print('Matchs data register correctly')
    except sqlite3.IntegrityError:
        print ('There was an error saving the matchs data')
    finally:
        conn.close()


def data_round(move, results, match): #TODO-----> PROBAR ESTE CODIGO
    '''Insert data to db round table---> match_idresults, move'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM match WHERE useid = ?", (match,))
        match_id_result = cursor.fetchone()
        if match_id_result is None:
            print("Match not found")
            return
        match_id = match_id_result[0]
        cursor.execute('''
                       INSERT INTO match (match_id, results, move) 
                       VALUES (?, ?, ?) 
                       ''', (match_id, results,  move))
        conn.commit()
        print('Round data register correctly')
    except sqlite3.IntegrityError:
        print ('There was an error saving the round data')
    finally:
        conn.close()


def delete_row():
    '''Pa eliminar weas'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM match
                   WHERE id=1''')
    # cursor.execute('''DROP TABLE IF EXISTS match_extended''')-----> guardar comando
    conn.commit()
    conn.close()


if __name__ == "__main__":
    #create_db()
    #create_table_user()
    #create_table_match()
    #create_table_round()
    user, email = start_match()
    win, fail, round, move = match()
    n_match = end_match()
    data_users_mail(user, email)
    data_users_game(n_match, win, fail, user)
    data_match(round, move, user)
    # delete_row()