import json
from pathlib import Path

JSON_FILE_PATH = Path("data/accounts.json")

class SessionAuth:
    @staticmethod
    def load_users():
        if JSON_FILE_PATH.exists():
            with open(JSON_FILE_PATH, "r") as file:
                data = json.load(file)
                return data.get("users", [])
        return []

    @staticmethod
    def save_users(users):
        with open(JSON_FILE_PATH, "w") as file:
            json.dump({"users": users}, file)

    @staticmethod
    def register_user(username, password, role="user"):
        users = SessionAuth.load_users()
        
        if any(user['username'] == username for user in users):
            return False, "Username sudah ada"
        
        users.append({
            'username': username,
            'password': password,
            'role': role
        })
        
        SessionAuth.save_users(users)
        return True, f"{role.capitalize()} Akun berhasil dibuat!"

    @staticmethod
    def authenticate(username, password):
        users = SessionAuth.load_users()
        
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)
        
        if user:
            return user
        return None

    @staticmethod
    def get_current_user(request):
        return request.session.get('current_user', None)

    @staticmethod
    def login(request, username, password):
        user = SessionAuth.authenticate(username, password)
        if user:
            request.session['current_user'] = user
            return True
        return False

    @staticmethod
    def logout(request):
        if 'current_user' in request.session:
            del request.session['current_user']