'''EXPLICA TU IMPORTACIÓN DE SQLite3'''
import sqlite3
import random


def create_db():
    '''Funcion para crear la base de datos'''
    conn = sqlite3.connect("rps.db")
    conn.commit()
    conn.close()


def create_table_user():
    '''Creamos la tabla usuarios'''
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
    '''Creamos la tabla partidas'''
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
    '''Inicio del juego'''
    #? 1. INTRODUCCIÓN AL JUEGO
    print("\n******* Rock Paper Scissors *******\n")
    user = input("Hi! What's your name? ").lower()
    email = input("Please, tell us your email ")
    print("\nGreat! You'll be playing against the machine")


def match():
    '''Lógica de una ronda'''
    #? 2. ELECCIÓN DEL USUARIO
    options = ['R', 'P', 'S'] #* Establecemos las opciones que tiene la máquina
    round_results = []
    score = 0
    for _ in range (3):
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
    print("\n******* RESULTS *******\n")
    print(f'The results are {round_results}. Your score is {score}\n')


def end_match():
    '''dsf'''
    while True:
        try:
            other_match = input('Do want to play again? Yes (Y) or No (N): ').upper()
            ['Y', 'N'].index(other_match)
            match()
        except ValueError:
            print("That is not an option. Try again")
        else:
            if other_match == 'N':
                print('Thanks')
                break
    



if __name__ == "__main__":
    #create_db()
    #create_table_user()
    #create_table_match()
    start_match()
    match()
    end_match()
