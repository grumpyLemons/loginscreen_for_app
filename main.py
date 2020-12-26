import json
from os import remove
from getpass import getpass

user_db = dict()
loggedin = False
nick = None


def init():
    global user_db
    try:
        with open("user_database.json") as file:
            user_db = json.load(file)
    except FileNotFoundError:
        pass


def save():
    global user_db
    with open("user_database.json", "w") as file:
        json.dump(user_db, file)


def check_cookie():
    global loggedin, nick, user_db
    try:
        with open("token") as token:
            content = token.read()
            if content in user_db.keys():
                loggedin = True
                nick = content
    except FileNotFoundError:
        pass


def save_cookie(auth=False):
    global nick
    if auth:
        with open("token", 'w') as token:
            token.write(nick)


def del_cookie(auth=False):
    if auth:
        try:
            remove("token")
        except FileNotFoundError:
            pass


def login(nickname, password):
    global loggedin, nick
    if nickname in user_db.keys():
        if password == user_db[nickname]['password']:
            loggedin = True
            nick = nickname
            print("Successfully logged in")
            choice = input("Remember password?(1 = yes): ")
            if choice == "1":
                save_cookie(loggedin)
                print("Password saved")
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
            choice = input("Remember password?(1 = yes): ")
            if choice == "1":
                save_cookie(loggedin)
                print("Password saved")
        except ValueError:
            print("Invalid type for experience")


def change_pwd(auth=False):
    global nick
    if auth:
        print("Change password:")
        old_pwd = getpass(prompt="Type in your old password: ")
        new_pwd = getpass(prompt="Type in your new password: ")
        if old_pwd == user_db[nick]["password"]:
            user_db[nick]["password"] = new_pwd
            save()
            print("Successfully changed your password")
        else:
            print("Wrong password")
    else:
        print("Access denied")


def change_nick(auth=False):
    global nick, loggedin
    if auth:
        print("Change username:")
        new_nick = input("Type in your new username: ")
        if new_nick not in user_db.keys():
            user_db[new_nick] = user_db[nick]
            del(user_db[nick])
            nick = new_nick
            save()
            save_cookie()
            print("Successfully changed your username")
        else:
            print("This username already exists")
    else:
        print("Access denied")


def profile(auth=False):
    global nick
    if auth:
        print(f"Hello, {user_db[nick]['name']} {user_db[nick]['surname']} ({nick})")
        print("What do you want to do? \n 1)Change password \n 2)Change username \n 3)Return \n 0)Log out")
        choice = input()
        while choice not in ["1", "2", "3", "0"]:
            choice = input()
        if choice == "1":
            change_pwd(auth)
            return True
        elif choice == "2":
            change_nick(auth)
            return True
        elif choice == "3":
            return False
        elif choice == "0":
            del_cookie(auth)
            return False

    else:
        print("Access denied")


def start(auth=False):
    global loggedin
    if not auth:
        print("What do you want to do? \n 1)Log in \n 2)Sign up \n 3)Exit")
        choice = input()
        while choice not in ["1", "2", "3"]:
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
        elif choice == "3":
            print("Goodbye!")
            exit(0)
    else:
        return False


def main():
    # Required part
    global loggedin
    init()
    while True:
        check_cookie()
        gb = start(loggedin)
        if not gb:
            break
    # Required part
    while True:
        tmp = profile(loggedin)
        if not tmp:
            break


main()