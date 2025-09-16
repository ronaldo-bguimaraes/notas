import re

import pandas as pd

from src.step import Step


class Padronizador(Step):
    def __init__(self, request):
        super().__init__(request)
        self.filepath = self.request["filepath"]

    @staticmethod
    def to_float(value: str):
        value = value.replace(".", "")
        value = value.replace(",", ".")
        value = re.sub("\\s+", "", value)
        return float(value)

    def handler(self):
        df = pd.read_parquet(self.filepath)
        df["chave"] = df["chave"].str.replace("\\s+", "", regex=True)
        df["item_cod"] = df["item_cod"].str.replace("\\s+", "", regex=True).str.extract(":(.+)\\)")

        df["item_valor"] = df["item_valor"].apply(self.to_float)
        df["item_total"] = df["item_total"].apply(self.to_float)

        df["empresa_cnpj"] = df["complemento"].str[0].str.replace("\\s+", "", regex=True).str.extract(":(.+)")
        df["empresa_cnpj"] = df["empresa_cnpj"].str.replace("\\D+", "", regex=True)

        df["empresa_endereco"] = df["complemento"].str[1].str.replace("\\s+", " ", regex=True)
        df["empresa_endereco"] = df["empresa_endereco"].str.replace("[\\s,]+,", ",", regex=True)

        df = df.drop(columns=["complemento"])

        print()
