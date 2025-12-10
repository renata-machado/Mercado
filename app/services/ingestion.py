import pandas as pd
from fastapi import UploadFile

class IngestionService:

    def _load_uploaded_csv(self, file: UploadFile) -> pd.DataFrame:
        return pd.read_csv(file.file)

    def load_estoque(self, file: UploadFile) -> pd.DataFrame:
        df = self._load_uploaded_csv(file)

        required_cols = {"produto", "quantidade", "custo_unitario"}
        if not required_cols.issubset(df.columns):
            raise ValueError(
                f"O arquivo de estoque deve conter as colunas: {required_cols}. "
                f"Encontrado: {set(df.columns)}"
            )

        return df

    def load_vendas(self, file: UploadFile) -> pd.DataFrame:
        df = self._load_uploaded_csv(file)

        required_cols = {"produto", "quantidade_vendida", "preco_unitario"}
        if not required_cols.issubset(df.columns):
            raise ValueError(
                f"O arquivo de vendas deve conter as colunas: {required_cols}. "
                f"Encontrado: {set(df.columns)}"
            )

        return df
