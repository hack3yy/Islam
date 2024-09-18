import json
import os

USERS_FILE = 'users.json'
FAVORITES_FILE_PREFIX = 'favorites_'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file)

def load_favorites(username):
    filename = f"{FAVORITES_FILE_PREFIX}{username}.json"
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        return json.load(file)

def save_favorites(username, favorites):
    filename = f"{FAVORITES_FILE_PREFIX}{username}.json"
    with open(filename, 'w') as file:
        json.dump(favorites, file)

def signup(username, password):
    users = load_users()
    if username in users:
        return False  # User already exists
    users[username] = password
    save_users(users)
    return True

def login(username, password):
    users = load_users()
    if username in users and users[username] == password:
        return True
    return False
