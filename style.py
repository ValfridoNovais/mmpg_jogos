# Arquivo: style.py

CSS_STYLE = """
<style>
/* Estilos para o layout principal */
[data-testid="stAppViewContainer"] {
    background-color: #F7F7F7; /* Cor de fundo para toda a página */
    padding: 0;
    margin: 0;
}

/* Estilização dos botões */
[data-testid="stButton"] {
    background-color: #4CAF50; /* Cor de fundo dos botões */
    color: white; /* Cor do texto dos botões */
    border-radius: 8px; /* Bordas arredondadas */
    padding: 10px 20px; /* Espaçamento interno */
    font-weight: bold; /* Texto em negrito */
}

[data-testid="stButton"]:hover {
    background-color: #45A049; /* Cor ao passar o mouse */
}

/* Estilização para as colunas do tabuleiro */
[data-testid="column"] {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 !important;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 2rem !important;
}

/* Estilização para tornar os botões quadrados */
[data-testid="stBaseButton"], [data-testid="stBaseButton-secondary"], [data-testid="stTooltipHoverTarget"] {
    aspect-ratio: 1 !important;
    width: 100% !important;
    height: auto !important;
    font-size: calc(2rem + 0.5vw) !important;
    margin: 5px !important;
    border-radius: 8px !important;
    padding: 0 !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}

/* Estilização da barra lateral */
[data-testid="stSidebar"] {
    background-color: #F7F7F7;
    padding: 20px;
}

[data-testid="stSidebar"] h2 {
    color: #4CAF50; /* Cor do título da barra lateral */
    font-weight: bold;
    text-align: center;
}
</style>
"""
