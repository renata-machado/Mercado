import pandas as pd


class AnalyticsService:
 

    @staticmethod
    def merge_estoque_vendas(df_estoque: pd.DataFrame, df_vendas: pd.DataFrame) -> pd.DataFrame:
        """
        Junta estoque e vendas pelo nome do produto.
        """
        df = pd.merge(df_estoque, df_vendas, on="produto", how="left")
        df["quantidade_vendida"] = df["quantidade_vendida"].fillna(0)
        df["preco_unitario"] = df["preco_unitario"].fillna(0)
        return df

    @staticmethod
    def calcular_metricas(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adiciona ao DataFrame as métricas principais:
        - Receita
        - Custo total
        - Lucro
        - Margem de lucro
        - Estoque remanescente
        """

        df["receita"] = df["quantidade_vendida"] * df["preco_unitario"]
        df["custo_total"] = df["quantidade"] * df["custo_unitario"]
        df["lucro"] = df["receita"] - (df["quantidade_vendida"] * df["custo_unitario"])

        df["estoque_atual"] = df["quantidade"] - df["quantidade_vendida"]

        df["margem_lucro"] = df.apply(
            lambda x: (x["lucro"] / x["receita"]) if x["receita"] > 0 else 0,
            axis=1
        )

        return df

    @staticmethod
    def resumo_geral(df: pd.DataFrame) -> dict:
        """
        Retorna métricas globais do negócio:
        - Receita total
        - Custo total
        - Lucro total
        - Margem global
        - Produtos com estoque zerado
        - Produtos mais vendidos
        """

        receita_total = df["receita"].sum()
        custo_total = (df["quantidade_vendida"] * df["custo_unitario"]).sum()
        lucro_total = receita_total - custo_total

        margem_global = lucro_total / receita_total if receita_total > 0 else 0

        produtos_sem_estoque = df[df["estoque_atual"] <= 0]["produto"].tolist()
        mais_vendidos = (
            df.sort_values(by="quantidade_vendida", ascending=False)
              [["produto", "quantidade_vendida"]]
              .head(5)
              .to_dict(orient="records")
        )

        return {
            "receita_total": receita_total,
            "custo_total": custo_total,
            "lucro_total": lucro_total,
            "margem_global": margem_global,
            "produtos_sem_estoque": produtos_sem_estoque,
            "top_5_mais_vendidos": mais_vendidos,
        }

    def processar(self, df_estoque: pd.DataFrame, df_vendas: pd.DataFrame) -> dict:
       
        df_merged = self.merge_estoque_vendas(df_estoque, df_vendas)
        df_metricas = self.calcular_metricas(df_merged)
        resumo = self.resumo_geral(df_metricas)

        return {
            "df_metricas": df_metricas,
            "resumo": resumo
        }


#camada de negocio