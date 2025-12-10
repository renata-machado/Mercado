from pydantic import BaseModel, Field


class ProductPromotionRequest(BaseModel):
    """
    Estrutura usada para solicitar a geração de uma promoção manual.
    """
    produto: str = Field(..., example="Arroz Tipo 1 5kg")
    preco_atual: float = Field(..., example=22.90, gt=0)
    preco_promocional: float = Field(..., example=19.90, gt=0)
    estoque: int = Field(..., example=120, ge=0)


class ProdutoMetricas(BaseModel):
    """
    Modelo opcional  para retornar métricas do algoritmo de analytics.
    """
    produto: str
    estoque_atual: int
    vendas_ultimos_dias: int
    score: float


#camada de acesso