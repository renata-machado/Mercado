import os
from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


DATA_DIR = BASE_DIR / "data"
CARDS_OUTPUT_DIR = BASE_DIR / "generated_cards"

# Criar pastas
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CARDS_OUTPUT_DIR, exist_ok=True)

#tipos de arquivo
VALID_EXTENSIONS = [".csv", ".xlsx"]

# Configurações da API
API_TITLE = "Mercado teste1"
API_DESCRIPTION = "Sistema para sugerir promoções baseado em estoque e vendas."
API_VERSION = "0.1.0"

# Configurações dos cards
CARD_WIDTH = 1080
CARD_HEIGHT = 1080
CARD_FONT_SIZE = 60
CARD_FONT_COLOR = (255, 255, 255)  
CARD_BACKGROUND_COLOR = (0, 0, 0)  
CARD_FONT_PATH = str(BASE_DIR / "assets" / "Roboto-Bold.ttf")

# Parâmetros do algoritmo de sugestão
HIGH_STOCK_THRESHOLD = 50        # estoque alto
LOW_SALES_THRESHOLD = 10         # vendas baixas
MIN_SCORE_TO_SUGGEST = 0.6       # score mínimo para sugerir promoção


#camada de negocio