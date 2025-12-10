from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime


class CardGeneratorService:
    
    

    OUTPUT_DIR = "generated_cards"

    def __init__(self):
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)

    @staticmethod
    def gerar_texto_oferta(produto: str, preco_atual: float, preco_promocional: float, estoque: int) -> str:
       
        desconto = 100 - ((preco_promocional / preco_atual) * 100)

        return (
            f"Promoção do dia!\n\n"
            f"Produto: {produto}\n"
            f"Preço original: R$ {preco_atual:.2f}\n"
            f"Preço promocional: R$ {preco_promocional:.2f}\n"
            f"Desconto: {desconto:.1f}%\n"
            f"Estoque disponível: {estoque} unidades\n\n"
            f"Aproveite enquanto durar o estoque!"
        )

    def gerar_card_imagem(
        self,
        produto: str,
        preco_atual: float,
        preco_promocional: float,
        caminho_arquivo: str = None
    ) -> str:
      

        largura = 1080
        altura = 1080

        img = Image.new("RGB", (largura, altura), color=(255, 230, 180))
        draw = ImageDraw.Draw(img)

        # Fonte padrão do PIL
        try:
            font_titulo = ImageFont.truetype("arial.ttf", 70)
            font_texto = ImageFont.truetype("arial.ttf", 45)
        except:
            font_titulo = ImageFont.load_default()
            font_texto = ImageFont.load_default()

        # Texto no card
        draw.text((50, 100), "OFERTA ESPECIAL", fill=(0, 0, 0), font=font_titulo)
        draw.text((50, 250), f"Produto: {produto}", fill=(0, 0, 0), font=font_texto)
        draw.text((50, 330), f"De: R$ {preco_atual:.2f}", fill=(120, 0, 0), font=font_texto)
        draw.text((50, 410), f"Por: R$ {preco_promocional:.2f}", fill=(0, 120, 0), font=font_texto)

        draw.text(
            (50, 550),
            "Aproveite enquanto durar o estoque!",
            fill=(0, 0, 0),
            font=font_texto
        )


        if caminho_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_arquivo = os.path.join(self.OUTPUT_DIR, f"card_{produto}_{timestamp}.png")

        img.save(caminho_arquivo)
        return caminho_arquivo

    def gerar_promocao_completa(self, produto: str, preco_atual: float, preco_promocional: float, estoque: int) -> dict:
      
        texto = self.gerar_texto_oferta(produto, preco_atual, preco_promocional, estoque)
        card_path = self.gerar_card_imagem(produto, preco_atual, preco_promocional)

        return {
            "texto_promocao": texto,
            "card_path": card_path
        }

#camada de negocio