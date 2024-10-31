'''Imports'''
import sqlite3
import random

# TODO -----> | EXTRAER LOS DATOS NECESARIOS | AÑADIR DATOS A TABLA | INYECCION DATOS |



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


def start_match():
    '''Start of the game'''
    #? 1. INTRODUCCIÓN AL JUEGO
    print("\n******* Rock Paper Scissors *******\n")
    user = input("Hi! What's your name? ").lower() 
    email = input("Please, tell us your email ")
    return user, email


def match():
    '''Logic for one match (3 rounds)'''
    #? 2. ELECCIÓN DEL USUARIO
    print("\nGreat! You'll be playing against the machine")
    options = ['R', 'P', 'S'] #* Establecemos las opciones que tiene la máquina
    round_results = []
    score = 0
    win = 0
    fail = 0
    round = 1   
    for _ in range (3):
        print(f'***** ROUND {round} *****\n')
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
    print(f'The results are {round_results}. Your score is {score}\n')
    if score >= 2:
        win += 1
        print("You won de game!!!")
    else:
        fail += 1
        print("The machine has won ")
    return win, fail, move

def end_match():
    '''Logic for the end of the game, deciding whether to play another game or not'''
    n_match = 0
    while True:
        try:
            other_match = input('Do want to play again? Yes (Y) or No (N): ').upper()
            ['Y', 'N'].index(other_match)
            if other_match == 'Y':
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


def data_user(user, email):
    '''Intento de insertar datos del usuario a la tabla users'''
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

    


if __name__ == "__main__":
    #create_db()
    #create_table_user()
    #create_table_match()
    user, email = start_match()
    match()
    n_match = end_match()
    #data_user(user, email)
