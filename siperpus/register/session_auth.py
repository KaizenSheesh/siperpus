# session_auth.py
class SessionAuth:
    @staticmethod
    def register_user(request, username, password, role):
        users = request.session.get('users', [])
        
        if any(user['username'] == username for user in users):
            return False, "Username already exists"
            
        users.append({
            'username': username,
            'password': password,
            'role': role
        })
        
        request.session['users'] = users
        return True, "Registration successful"

    @staticmethod
    def authenticate(request, username, password):
        users = request.session.get('users', [])
        
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)
        
        if user:
            request.session['current_user'] = user
            return True
        return False

    @staticmethod
    def get_current_user(request):
        return request.session.get('current_user', None)    

    @staticmethod
    def logout(request):
        if 'current_user' in request.session:
            del request.session['current_user']