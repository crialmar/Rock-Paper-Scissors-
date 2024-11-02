'''Imports'''
import sqlite3
import random
import smtplib


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


def start_match(): #TODO REGISTER
    '''Start of the game'''
    #? 1. INTRODUCCIÓN AL JUEGO
    print("\n******* Rock Paper Scissors *******\n")
    user = input("Hi! What's your name? ").lower()
    email = input("Please, tell us your email: ")
    return user, email


def match(user):
    '''Logic for one match (3 rounds)'''
    #? 2. ELECCIÓN DEL USUARIO
    print("\nGreat! You'll be playing against the machine")
    options = ['R', 'P', 'S'] #* Establecemos las opciones que tiene la máquina
    round_results = []
    move_human = []
    match_final = []
    score = 0
    round_n = 0
    for _ in range (3):
        print('***** FIGHT *****\n')
        while True:
            try:
                move = input("Choose an option: Rock (R), Paper (P) or Scissors (S) ").upper()
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
        move_human.append(move)
        print(move_human)
        round_n += 1
    print("\n******* RESULTS *******\n")
    print(f'The results are {round_results}. Your score is {score}')
    win = 0
    fail = 0
    if score >= 2:
        win += 1
        match_final.append('Win')
        print("You won the game!!!\n")
    else:
        fail += 1
        match_final.append('Fail')
        print("The machine has won\n")
    data_match(round_n, user, match_final)
    get_id_match()
    data_round(round_results, move_human)
    return win, fail, round_n, round_results, move_human, match_final


def data_match(round_n, user, match_final):
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
        for fin in match_final:
            cursor.execute('''
                       INSERT INTO match (user_id, rounds, results) 
                       VALUES (?, ?, ?) 
                       ''', (user_id, round_n, fin))
        conn.commit()
        print('Matchs data register correctly')
    except sqlite3.IntegrityError:
        print ('There was an error saving the matchs data')
    finally:
        conn.close()
    return user_id


def get_id_match():
    '''Get the matchs id'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT MAX(id) FROM match''')
        match_id_ = cursor.fetchone()
        if match_id_ is None:
            print("Match not found")
            conn.commit()
            print(f'SOY EL ID DEL MATCH {match_id_}')
        else:
            match_id_ = match_id_[0]
        return match_id_
    except sqlite3.IntegrityError:
        print ('There was an error creating or getting the match')
    finally:
        conn.close()


def data_round(round_results, move_human):
    '''Insert data to db round table---> match_id, results, move'''
    match_id = get_id_match()
    if match_id is None:
        print('Error: no match created or obtained')
    print(f'Soy el gran y único MATCH ID {match_id}')
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    try:
        for result, move in zip(round_results, move_human):
            cursor.execute('''
                            INSERT INTO round (match_id, results, move) 
                            VALUES (?, ?, ?) 
                                ''', (match_id, result, move))
            conn.commit()
            print('Round data register correctly')
    except sqlite3.IntegrityError:
        print ('There was an error saving the round data')
    finally:
        conn.close()


def end_match(user):
    '''Logic for the end of the game, deciding whether to play another game or not'''
    n_match = 0
    while True:
        try:
            other_match = input('Do want to play again? Yes (Y) or No (N): ').upper()
            ['Y', 'N'].index(other_match)
            if other_match == 'Y':
                # total_round = round + {round}
                n_match += 1
                
                match(user)
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


def delete_row():
    '''Pa eliminar weas'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM match
                   WHERE id=1''')
    # cursor.execute('''DROP TABLE IF EXISTS match_extended''')-----> guardar comando
    conn.commit()
    conn.close()


def get_match_total(user, n_match):
    '''Get all match'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT id FROM users WHERE user=?''', (user,))
        user_id_result = cursor.fetchone()[0]
        if user_id_result is None:
            print('NO USER')
            return None
        cursor.execute('''SELECT COUNT(*) FROM match WHERE user_id=?''', (n_match,))
        match_count = cursor.fetchone()[0]
        print(f'{user}s matches: {match_count}')
        return match_count
    except sqlite3.IntegrityError:
        print ('pos no lo conseguiste')
    finally:
        conn.close()


def get_win_fail(user_id):
    '''Get number of matches won and failed'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT COUNT(*) FROM match WHERE user_id=? AND results="Win"''', (user_id,))
        win_count = cursor.fetchone()[0]
        print(f'Win {win_count} veces')
        cursor.execute('''SELECT COUNT(*) FROM match WHERE user_id=? AND results="Fail"''', (user_id,))
        fail_count = cursor.fetchone()[0]
        print(f'Fail {fail_count} veces')
        return win_count, fail_count
    except sqlite3.IntegrityError:
        print ('pos no lo conseguiste')
    finally:
        conn.close()


def calculate_winrate(match_count, win_count):
    '''Function to calculate the winrate'''
    win_count_int = win_count[0]
    winrate = round((win_count_int/match_count)*100)
    print(f'Your winrate is: {winrate}%')


def get_best_move(user_id, match_count):
    '''Get the best move'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT move, COUNT(move) AS win_count
                          FROM round 
                          WHERE match_id IN (SELECT id FROM match WHERE user_id=? AND results="Win")
                          GROUP BY move
                          ORDER BY win_count DESC
                          LIMIT 1''', (user_id,))
        best_winning_move = cursor.fetchone()
        if best_winning_move:
            winrate_best_move = round((best_winning_move[1]/match_count)*100)
            print(f'La jugada con más victorias es {best_winning_move[0]} con un winrate de {winrate_best_move}% ({best_winning_move[1]} victorias).')
            return best_winning_move[0]
        else:
            print("No se encontraron jugadas ganadoras y perdedoras para el usuario.")
    except sqlite3.IntegrityError:
        print("Error al obtener la mejor y peor jugada ganadora.")
    finally:
        conn.close()


def get_worst_move(user_id, match_count):
    '''Get the worst move'''
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT move, COUNT(move) AS win_count
                          FROM round 
                          WHERE match_id IN (SELECT id FROM match WHERE user_id=? AND results="Fail")
                          GROUP BY move
                          ORDER BY win_count DESC
                          LIMIT 1''', (user_id,))
        worst_winning_move = cursor.fetchone()
        if worst_winning_move:
            winrate_worst_move = round((worst_winning_move[1]/match_count)*100)
            print(f'La jugada con más fail es {worst_winning_move[0]} con un winrate de {winrate_worst_move}% ({worst_winning_move[1]} fail).')
            return worst_winning_move[0]
        else:
            print("No se encontraron jugadas ganadoras y perdedoras para el usuario.")
    except sqlite3.IntegrityError:
        print("Error al obtener la mejor y peor jugada ganadora.")
    finally:
        conn.close()


def send_email(email, match_count, win_count, fail_count, winrate, best_winning_move, worst_winning_move): #TODO 
    '''Send email----> match'''
    sender = 'crythonjs@gmail.com'
    sPass = 'passrps1'
    addressee = {email}
    

if __name__ == "__main__":
    #create_db()
    #create_table_user()
    #create_table_match()
    #create_table_round()
    user, email = start_match()
    win, fail, round_n, round_results, move_human, match_final = match(user)
    user_id = data_match(round_n, user, match_final)
    n_match = end_match(user)
    match_count= get_match_total(user, n_match)
    win_count = get_win_fail(user_id)
    data_users_mail(user, email)
    data_users_game(n_match, win, fail, user)
    get_match_total(user, n_match)
    get_win_fail(user_id)
    calculate_winrate(match_count, win_count)
    get_best_move(user_id, match_count)
    get_worst_move(user_id, match_count)
    # delete_row()
