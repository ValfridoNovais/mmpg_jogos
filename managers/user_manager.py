import json
import hashlib  # Para hash da senha

class UserManager:
    def __init__(self, file_path='pages/js/users.json'):
        self.file_path = file_path
        self.users = self.load_users()

    def load_users(self):
        """Carrega os usuários do arquivo JSON."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get("users", {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_users(self):
        """Salva os usuários no arquivo JSON."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({"users": self.users}, file, indent=4, ensure_ascii=False)

    def hash_password(self, password):
        """Gera um hash SHA256 para a senha."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, name, password, email):
        """Registra um novo usuário."""
        if username in self.users:
            return "Usuário já cadastrado."
        
        hashed_password = self.hash_password(password)
        self.users[username] = {
            "name": name,
            "password": hashed_password,
            "email": email
        }
        self.save_users()
        return "Cadastro realizado com sucesso!"

    def authenticate_user(self, username, password):
        """Valida o login do usuário."""
        user = self.users.get(username)
        if user and user["password"] == self.hash_password(password):
            return True
        return False
