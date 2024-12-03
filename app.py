import streamlit as st
from managers.user_manager import UserManager  # Gerenciador de usuários
from managers.game_manager import GameManager  # Gerenciador de partidas
from managers.room_manager import RoomManager  # Gerenciador de salas
from managers.ranking_manager import RankingManager  # Gerenciador de rankings
from style import CSS_STYLE
import time

# Aplica o CSS personalizado
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# Configurações do repositório GitHub
REPO_NAME = "ValfridoNovais/mmpg_jogos"
BRANCH = "main"
TOKEN = st.secrets["GITHUB_TOKEN"]

# Inicializa os gerenciadores
user_manager = UserManager(file_path='pages/js/users.json')
game_manager = GameManager(file_path='pages/js/games.json', repo_name=REPO_NAME, branch=BRANCH, token=TOKEN)
ranking_manager = RankingManager(file_path='pages/js/ranking.json', repo_name=REPO_NAME, branch=BRANCH, token=TOKEN)
room_manager = RoomManager(file_path='pages/js/rooms.json')  # Gerenciador de salas

# Função para exibir a tela de login/cadastro
def show_auth():
    st.title("Bem-vindo ao Jogo da Velha Multiplayer!")
    st.write("Por favor, faça login ou cadastre-se para começar a jogar.")
    
    menu = st.radio("Escolha uma opção:", ["Login", "Cadastro"])

    if menu == "Login":
        st.subheader("Login")
        username = st.text_input("Usuário:")
        password = st.text_input("Senha:", type="password")
        if st.button("Entrar"):
            if user_manager.authenticate_user(username, password):
                st.success(f"Bem-vindo de volta, {username}!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

    elif menu == "Cadastro":
        st.subheader("Cadastro")
        name = st.text_input("Nome:")
        username = st.text_input("Usuário:")
        email = st.text_input("Email:")
        password = st.text_input("Senha:", type="password")
        if st.button("Cadastrar"):
            if name and username and email and password:
                message = user_manager.register_user(username, name, password, email)
                st.success(message)
            else:
                st.error("Por favor, preencha todos os campos!")

# Menu principal
def main():
    st.sidebar.header("Menu")
    menu = st.sidebar.radio("Navegação", ["Início", "Salas", "Ranking"])

    if menu == "Início":
        show_home()
    elif menu == "Salas":
        if "current_room" in st.session_state and st.session_state["current_room"] is not None:
            handle_room()
        else:
            show_rooms()
    elif menu == "Ranking":
        show_ranking()

# Página inicial
def show_home():
    st.title("Bem-vindo ao Jogo da Velha Multiplayer!")
    st.write(f"""
        Este é um aplicativo de Jogo da Velha com suporte a partidas multijogador.
        Você está logado como **{st.session_state['username']}**.
        Use o menu na barra lateral para navegar entre as opções.
    """)

# Página de salas
def show_rooms():
    st.title("Salas de Jogo")
    for room in room_manager.rooms:
        st.subheader(room["name"])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Jogar", key=f"join_{room['room_id']}", disabled="Aguardando jogador..." not in room["players"]):
                if room_manager.join_room(room["room_id"], st.session_state["username"]):
                    st.session_state["current_room"] = room["room_id"]
                    st.rerun()
        with col2:
            if st.button("Ver", key=f"view_{room['room_id']}"):
                room_manager.log_access(room["room_id"], st.session_state["username"], "Visualizador")
                st.session_state["current_room"] = room["room_id"]
                st.rerun()

# Gerenciar uma sala
def handle_room():
    room_id = st.session_state["current_room"]
    room = next((r for r in room_manager.rooms if r["room_id"] == room_id), None)

    if room:
        st.title(f"Jogando na {room['name']}")

        # Se o jogador for um dos jogadores da sala
        if st.session_state["username"] in room["players"]:
            st.write("Você está jogando!")
            show_game(room_id)  # Passa o ID da sala para a lógica do jogo
        else:
            st.write("Você está visualizando esta sala.")
            show_game_view(room_id)  # Exibe apenas o tabuleiro

        if st.button("Sair da Sala"):
            room_manager.leave_room(st.session_state["current_room"], st.session_state["username"])
            st.session_state["current_room"] = None
            st.rerun()

# Página de jogo
def show_game(room_id):
    room = next((r for r in room_manager.rooms if r["room_id"] == room_id), None)
    if not room:
        st.error("Sala não encontrada.")
        return

    st.subheader(f"Partida na {room['name']}")
    st.write(f"Jogadores: {room['players'][0]} (X) vs {room['players'][1]} (O)")

    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            index = i * 3 + j
            with cols[j]:
                button_label = room["board"][index] if room["board"][index] != " " else " "
                if st.button(button_label, key=f"btn_{room_id}_{index}"):
                    if (
                        room["board"][index] == " "
                        and st.session_state["username"] == room["players"][0 if room["current_player"] == "X" else 1]
                    ):
                        room["board"][index] = room["current_player"]
                        room["current_player"] = "O" if room["current_player"] == "X" else "X"
                        room_manager.save_rooms()

                        winner = check_winner(room["board"])
                        if winner:
                            st.success(f"{room['players'][0 if winner == 'X' else 1]} venceu!")
                            room["winner"] = winner
                            room_manager.save_rooms()
                        elif " " not in room["board"]:
                            st.info("Empate!")
                            room["winner"] = "Empate"
                            room_manager.save_rooms()
                        st.rerun()

# Exibir tabuleiro apenas para visualizadores
def show_game_view(room_id):
    room = next((r for r in room_manager.rooms if r["room_id"] == room_id), None)
    if not room:
        st.error("Sala não encontrada.")
        return

    st.subheader(f"Visualizando a {room['name']}")
    st.write(f"Jogadores: {room['players'][0]} (X) vs {room['players'][1]} (O)")
    cols = st.columns(3)
    for i in range(3):
        for j in range(3):
            index = i * 3 + j
            with cols[j]:
                button_label = room["board"][index] if room["board"][index] != " " else " "
                st.button(button_label, key=f"view_{room_id}_{index}", disabled=True)

# Verificar vencedor
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != " ":
            return board[combo[0]]
    return None

# Página de ranking
def show_ranking():
    st.title("Ranking")
    ranking = ranking_manager.get_ranking()
    if ranking:
        st.table([
            {
                "Posição": idx + 1,
                "Jogador": player_name,
                "Pontos": stats["points"],
                "Vitórias": stats["wins"],
                "Empates": stats["draws"],
                "Derrotas": stats["losses"],
            }
            for idx, (player_name, stats) in enumerate(ranking)
        ])
    else:
        st.info("Nenhum jogador registrado no ranking ainda.")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    show_auth()
else:
    main()
