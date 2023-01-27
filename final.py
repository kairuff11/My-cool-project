import calendar
from datetime import date
import shelve

class Workout:
    def __init__(self):
        self.users = []
        self.passwords = []
        self.workouts = {}

    def login(self, u, p):
        with shelve.open('workout') as db:
            if 'users' in db:
                self.users = db['users']
                self.passwords = db['passwords']
            if 'workouts' in db:
                self.workouts = db['workouts']

        found = -1
        for i in range(len(self.users)):
            if u == self.users[i]:
                found = i
                break
        if found >= 0 and p == self.passwords[i]:
            return True
        return False

    def create_account(self, u, p):
        with shelve.open('workout') as db:
            if 'users' in db:
                self.users = db['users']
                self.passwords = db['passwords']
            self.users.append(u)
            self.passwords.append(p)
            db['users'] = self.users
            db['passwords'] = self.passwords
            self.workouts[u] = {}
            db['workouts'] = self.workouts

    def menu(self):
          while True:
            choice = input('Type 1 to create account or 2 to login: ')
            u = input('Enter username: ')
            p = input('Enter password: ')
            if choice == '1':
                self.create_account(u, p)
            elif choice == '2':
                if self.login(u, p):
                    while True:
                        action = input("What would you like to do? (1) view workouts (2) add workouts (3) log out: ")
                        if action == '1':
                            self.view_workouts(u)
                        elif action == '2':
                            self.add_workouts(u)
                        elif action == '3':
                            break
          print('logged out')

    def cypher(self, target, shift):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for index in range(len(alphabet)):
            if alphabet[index] == target:
                x = index + shift
                y = x % len(alphabet)
                return (alphabet[y])

    def encrypt(self, password):
        shift = 3
        encrypted_string = ''
        for x in password:
            if x == ' ':
                encrypted_string += ' '
            else:
                encrypted_string += self.cypher(x, shift)
        return (encrypted_string)

    def view_workouts(self, u):
        with shelve.open('workout') as db:
          if 'workouts' in db:
              self.workouts = db['workouts']
              if u in self.workouts:
                  for date, workout in self.workouts[u].items():
                    print(f"{date}:{workout}")
                    db['workouts'] = self.workouts

    def add_workouts(self, u):
        workout_name = input("Enter the name of the workout: ")
        workout_duration = input("Enter the duration of the workout: ")
        workout_date = input("Enter the date of the workout (YYYY-MM-DD): ")
        with shelve.open('workout') as db:
            if 'workouts' in db:
                self.workouts = db['workouts']
                if u in self.workouts:
                    if workout_date in self.workouts[u]:
                        self.workouts[u][workout_date].append((workout_name, workout_duration))
                    else:
                        self.workouts[u][workout_date] = [(workout_name, workout_duration)]
                    db['workouts'] = self.workouts




workouts = Workout()
workouts.menu()
