# session_auth.py
class SessionAuth:
    @staticmethod
    def register_user(request, username, password, role):
        # Get existing users from session or initialize empty list
        users = request.session.get('users', [])
        
        # Check if username already exists
        if any(user['username'] == username for user in users):
            return False, "Username already exists"
            
        # Add new user
        users.append({
            'username': username,
            'password': password,  # Dalam implementasi nyata, password harus di-hash
            'role': role
        })
        
        # Update session
        request.session['users'] = users
        return True, "Registration successful"

    @staticmethod
    def authenticate(request, username, password):
        users = request.session.get('users', [])
        
        # Find user
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)
        
        if user:
            # Store current user in session
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