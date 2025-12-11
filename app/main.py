from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import uuid
import os
from app.services.ingestion import IngestionService
from app.services.analytics import AnalyticsService
from app.services.card_generator import CardGeneratorService
from app.models.schemas import ProductPromotionRequest


app = FastAPI(
    title="Super mercado teste1",
    description="API para sugerir produtos em oferta e gerar cards automaticamente.",
    version="1.0.0"
)


# Serviços
ingestion_service = IngestionService()
analytics_service = AnalyticsService()
card_service = CardGeneratorService()






@app.post("/upload-dados")
async def upload_dados(
    estoque_csv: UploadFile = File(...),
    vendas_csv: UploadFile = File(...)
):
    try:
        df_estoque = ingestion_service.load_estoque(estoque_csv.file)
        df_vendas = ingestion_service.load_vendas(vendas_csv.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler planilhas: {str(e)}")

    return {"status": "OK", "rows_estoque": len(df_estoque), "rows_vendas": len(df_vendas)}



@app.post("/analisar")
async def analisar(
    estoque_csv: UploadFile = File(...),
    vendas_csv: UploadFile = File(...)
):
    try:
        df_estoque = ingestion_service.load_estoque(estoque_csv.file)
        df_vendas = ingestion_service.load_vendas(vendas_csv.file)

        resultado = analytics_service.processar(df_estoque, df_vendas)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro no processamento: {str(e)}")

    return {
        "resumo": resultado["resumo"]
    }


#promoção manual
@app.post("/gerar-promocao")
async def gerar_promocao(dados: ProductPromotionRequest):
    try:
        resultado = card_service.gerar_promocao_completa(
            produto=dados.produto,
            preco_atual=dados.preco_atual,
            preco_promocional=dados.preco_promocional,
            estoque=dados.estoque,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar card: {str(e)}")

    return resultado


@app.post("/pipeline-completo")
async def pipeline_completo(
    estoque_csv: UploadFile = File(...),
    vendas_csv: UploadFile = File(...)
):
    try:
        # carregar arquivo enviado pelo usuário
        df_estoque = ingestion_service.load_estoque(estoque_csv)
        df_vendas = ingestion_service.load_vendas(vendas_csv)

        #  Análise
        resultado = analytics_service.processar(df_estoque, df_vendas)
        df_metricas = resultado["df_metricas"]

        # Selecionar produto com maior estoque 
        produto_escolhido = df_metricas.sort_values(
            by="estoque_atual", ascending=False
        ).iloc[0]

        produto = produto_escolhido["produto"]
        preco = produto_escolhido["preco_unitario"]
        estoque = int(produto_escolhido["estoque_atual"])

        # promoção automática
        preco_promocional = preco * 0.90

        promocao = card_service.gerar_promocao_completa(
            produto=produto,
            preco_atual=preco,
            preco_promocional=preco_promocional,
            estoque=estoque
        )

        

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no pipeline completo: {str(e)}")

    return {
        "produto_selecionado": produto,
        "estoque": estoque,
        "preco_atual": preco,
        "preco_promocional": preco_promocional,
        "resumo": resultado["resumo"],
        "promo": promocao
    }

#camada de acesso