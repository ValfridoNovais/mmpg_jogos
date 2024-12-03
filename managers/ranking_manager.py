import json  # Para manipular arquivos JSON
from github import Github  # Para sincronizar com o GitHub


class RankingManager:
    def __init__(self, file_path='pages/js/ranking.json', repo_name='', branch='main', token=''):
        """
        Inicializa o gerenciador de ranking.
        :param file_path: Caminho do arquivo JSON local que armazena o ranking.
        :param repo_name: Nome do repositório no GitHub (ex: 'usuario/repo').
        :param branch: Nome da branch do repositório (ex: 'main').
        :param token: Token de acesso pessoal do GitHub.
        """
        self.file_path = file_path
        self.repo_name = repo_name
        self.branch = branch
        self.token = token
        self.ranking = self.load_ranking()

    def load_ranking(self):
        """
        Carrega o ranking do arquivo JSON.
        :return: Um dicionário contendo o ranking ou vazio, caso o arquivo não exista.
        """
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_ranking(self):
        """
        Salva o ranking atualizado no arquivo JSON e no GitHub.
        """
        # Salva no arquivo local
        with open(self.file_path, 'w') as file:
            json.dump(self.ranking, file, indent=4)

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
                    message="Atualizando ranking.json via Streamlit",
                    content=content,
                    sha=contents.sha,
                    branch=self.branch,
                )
                print("Ranking atualizado no GitHub!")
            except Exception as e:
                print(f"Erro ao atualizar o arquivo no GitHub: {e}")

    def update_player(self, player_name, result):
        """
        Atualiza o ranking de um jogador com base no resultado do jogo.
        :param player_name: Nome do jogador.
        :param result: Resultado do jogo (win, draw, loss).
        """
        if player_name not in self.ranking:
            self.ranking[player_name] = {"points": 0, "wins": 0, "draws": 0, "losses": 0}

        if result == "win":
            self.ranking[player_name]["points"] += 3
            self.ranking[player_name]["wins"] += 1
        elif result == "draw":
            self.ranking[player_name]["points"] += 1
            self.ranking[player_name]["draws"] += 1
        elif result == "loss":
            self.ranking[player_name]["losses"] += 1

        self.save_ranking()

    def get_ranking(self):
        """
        Retorna o ranking ordenado por pontos.
        :return: Lista de jogadores ordenados por pontos.
        """
        return sorted(
            self.ranking.items(),
            key=lambda x: x[1]["points"],
            reverse=True,
        )
