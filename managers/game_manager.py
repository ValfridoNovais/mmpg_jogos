import json  # Para manipular arquivos JSON
import uuid  # Para gerar IDs únicos para os jogos
from github import Github  # Para sincronizar com o GitHub


class GameManager:
    def __init__(self, file_path='pages/js/games.json', repo_name='', branch='main', token=''):
        """
        Inicializa o gerenciador de partidas.
        :param file_path: Caminho do arquivo JSON local que armazena as partidas.
        :param repo_name: Nome do repositório no GitHub (ex: 'usuario/repo').
        :param branch: Nome da branch do repositório (ex: 'main').
        :param token: Token de acesso pessoal do GitHub.
        """
        self.file_path = file_path
        self.repo_name = repo_name
        self.branch = branch
        self.token = token
        self.games = self.load_games()

    def load_games(self):
        """
        Carrega o estado das partidas do arquivo JSON.
        :return: Um dicionário contendo as partidas ou vazio, caso o arquivo não exista.
        """
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file).get("games", {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_games(self):
        """
        Salva o estado atualizado das partidas no arquivo JSON e no GitHub.
        """
        # Salva no arquivo local
        with open(self.file_path, 'w') as file:
            json.dump({"games": self.games}, file, indent=4)

        # Sincroniza com o GitHub
        if self.repo_name and self.token:
            try:
                g = Github(self.token)
                repo = g.get_repo(self.repo_name)
                contents = repo.get_contents(self.file_path, ref=self.branch)
                with open(self.file_path, 'r') as file:
                    content = file.read()
                repo.update_file(
                    path=contents.path,
                    message="Atualizando games.json via Streamlit",
                    content=content,
                    sha=contents.sha,
                    branch=self.branch,
                )
                print("Estado das partidas atualizado no GitHub!")
            except Exception as e:
                print(f"Erro ao atualizar o arquivo no GitHub: {e}")

    def initialize_game(self, player1, player2):
        """
        Cria uma nova partida com os jogadores fornecidos.
        :param player1: Nome do jogador 1.
        :param player2: Nome do jogador 2.
        :return: ID único da partida criada.
        """
        game_id = str(uuid.uuid4())
        self.games[game_id] = {
            "board": [" "] * 9,  # Tabuleiro vazio
            "current_player": "X",  # Jogador inicial
            "players": [player1, player2],  # Lista de jogadores
            "winner": None,  # Inicialmente sem vencedor
        }
        self.save_games()
        return game_id

    def get_game(self, game_id):
        """
        Recupera o estado de uma partida específica.
        :param game_id: ID da partida.
        :return: Estado da partida ou None se o ID não existir.
        """
        return self.games.get(game_id)

    def update_game(self, game_id, board, current_player, winner=None):
        """
        Atualiza o estado de uma partida.
        :param game_id: ID da partida.
        :param board: Estado atualizado do tabuleiro.
        :param current_player: Próximo jogador.
        :param winner: Vencedor da partida (se houver).
        """
        if game_id in self.games:
            self.games[game_id].update({
                "board": board,
                "current_player": current_player,
                "winner": winner,
            })
            self.save_games()

    def delete_game(self, game_id):
        """
        Remove uma partida do estado.
        :param game_id: ID da partida.
        """
        if game_id in self.games:
            del self.games[game_id]
            self.save_games()
