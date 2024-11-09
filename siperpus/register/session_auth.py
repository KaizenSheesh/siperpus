import json
from pathlib import Path

# Path ke file JSON
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
        
        # Check if username already exists
        if any(user['username'] == username for user in users):
            return False, "Username already exists"
        
        # Add new user
        users.append({
            'username': username,
            'password': password,  # In real cases, make sure to hash passwords
            'role': role
        })
        
        # Save updated users list to JSON
        SessionAuth.save_users(users)
        return True, f"{role.capitalize()} account created successfully"
    
    @staticmethod
    def delete_user(username):
        users = SessionAuth.load_users()
        
        # Remove user by username
        users = [user for user in users if user['username'] != username]
        
        # Save updated users list to JSON
        SessionAuth.save_users(users)
        return True, "Account deleted successfully"

    @staticmethod
    def authenticate(username, password):
        users = SessionAuth.load_users()
        
        # Find user by username and password
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)
        
        if user:
            # Return the full user dictionary, including role
            return user
        return None

    @staticmethod
    def get_current_user(request):
        # Return the full user object from session
        return request.session.get('current_user', None)

    @staticmethod
    def login(request, username, password):
        user = SessionAuth.authenticate(username, password)
        if user:
            # Set the full user data, including role, in session
            request.session['current_user'] = user
            return True
        return False

    @staticmethod
    def logout(request):
        if 'current_user' in request.session:
            del request.session['current_user']