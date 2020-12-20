import json
from getpass import getpass

user_db = dict()
loggedin = False
nick = None


def init():
    global user_db
    with open("user_database.json") as file:
        user_db = json.load(file)


def save():
    global user_db
    with open("user_database.json", "w") as file:
        json.dump(user_db, file)


def login(nickname, password):
    global loggedin, nick
    if nickname in user_db.keys():
        if password == user_db[nickname]['password']:
            loggedin = True
            nick = nickname
            print("Successfully logged in")
        else:
            print("Incorrect password")
    else:
        print("This nickname does not exist")


def signup():
    global loggedin, nick
    nickname = input("Type in your nickname:")
    password = getpass(prompt="Type in your password:")
    name = input("Type in your name:")
    surname = input("Type in your surname:")
    experience = input("Type in how many problems have you solved in python: ")
    if nickname in user_db.keys():
        print("This nickname is already used")
    else:
        try:
            experience = int(experience)
            user_db[nickname] = {'password': password, 'name': name, 'surname': surname, 'experience': experience}
            save()
            loggedin = True
            nick = nickname
        except ValueError:
            print("Invalid type for experience")


def profile(auth=False):
    global nick
    if auth:
        print(f"Hello, {user_db[nick]['name']} {user_db[nick]['surname']} ({nick})")
    else:
        print("Access denied")


def start():
    global loggedin
    print("What do you want to do? \n 1)Log in \n 2)Sign up")
    choice = input()

    if choice == '1':
        while not loggedin:
            nickname = input("Please type in your nickname: ")
            password = getpass(prompt="Password: ")
            login(nickname, password)
            if not loggedin:
                if input("If you want to go back, type 1: ") == "1":
                    break
        else:
            return False
        return True

    elif choice == '2':
        while not loggedin:
            signup()
            if not loggedin:
                if input("If you want to go back, type 1: ") == "1":
                    break
        else:
            return False
        return True


def main():
    global loggedin
    init()
    while True:
        gb = start()
        if not gb:
            break
    profile(loggedin)


main()
