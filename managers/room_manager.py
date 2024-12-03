import json
from datetime import datetime

class RoomManager:
    def __init__(self, file_path='rooms.json'):
        self.file_path = file_path
        self.rooms = self.load_rooms()

    def load_rooms(self):
        """Carrega as salas do arquivo JSON."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)["rooms"]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_rooms(self):
        """Salva as salas no arquivo JSON."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({"rooms": self.rooms}, file, indent=4, ensure_ascii=False)

    def log_access(self, room_id, username, status):
        """Registra o acesso à sala."""
        room = next((r for r in self.rooms if r["room_id"] == room_id), None)
        if room:
            access_log = {
                "username": username,
                "status": status,
                "access_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "exit_time": None
            }
            room["access_log"].append(access_log)
            self.save_rooms()

    def update_exit_time(self, room_id, username):
        """Atualiza o horário de saída de um usuário."""
        room = next((r for r in self.rooms if r["room_id"] == room_id), None)
        if room:
            for log in room["access_log"]:
                if log["username"] == username and log["exit_time"] is None:
                    log["exit_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_rooms()
                    break

    def join_room(self, room_id, username):
        """Adiciona um jogador ou visualizador à sala."""
        room = next((r for r in self.rooms if r["room_id"] == room_id), None)
        if room:
            if username not in room["players"] and username not in room["viewers"]:
                if "Aguardando jogador..." in room["players"]:
                    room["players"][room["players"].index("Aguardando jogador...")] = username
                    self.log_access(room_id, username, "Jogador")
                else:
                    room["viewers"].append(username)
                    self.log_access(room_id, username, "Visualizador")
                self.save_rooms()
                return True
        return False

    def leave_room(self, room_id, username):
        """Remove um jogador ou visualizador da sala."""
        room = next((r for r in self.rooms if r["room_id"] == room_id), None)
        if room:
            if username in room["players"]:
                room["players"][room["players"].index(username)] = "Aguardando jogador..."
            elif username in room["viewers"]:
                room["viewers"].remove(username)
            self.update_exit_time(room_id, username)
            self.save_rooms()
