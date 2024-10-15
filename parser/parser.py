import json
import os
import re
from pathlib import Path
from typing import Optional, Dict

import pandas as pd
from bs4 import BeautifulSoup

from src.step import Step


class Parser(Step):
    def __init__(self, request):
        super().__init__(request)
        self.filepath = self.request["filepath"]
        self.soup: Optional[BeautifulSoup] = None
        self.data = []
        self.row = {}

    def save_line(self):
        new_row = self.row.copy()
        self.data.append(new_row)

    def update_values(self, mapper: Dict):
        self.row.update(mapper)

    def save_values(self, mapper: Dict):
        self.update_values(mapper)
        self.save_line()

    def handler(self):
        with open(self.filepath, mode="rb") as file:
            buffer = file.read()

        self.soup = BeautifulSoup(buffer, "html.parser")

        self.parse()

        foldename = f"/tmp/parseado"
        os.makedirs(foldename, exist_ok=True)
        filename = Path(self.filepath).stem + "_parsed.parquet"
        filepath = Path(foldename, filename)

        df = pd.DataFrame.from_records(self.data)
        df.to_parquet(filepath, engine="pyarrow")

        return {
            "filepath": str(filepath.resolve())
        }

    def parse(self):
        header = []
        for node in self.soup.select("#conteudo .txtCenter .text"):
            header.append(node.text)

        self.update_values({
            "empresa": self.soup.select_one("#conteudo .txtCenter .txtTopo").text,
            "chave": self.soup.select_one("span.chave").text,
            "complemento": header,
        })

        infos = self.soup.select_one("#infos").text
        self.update_values({
            "numero": re.search("N.mero\\D+(\\d+)", infos).group(1),
            "serie": re.search("S.rie\\D+(\\d+)", infos).group(1),
            "emissao": re.search("Emiss.o\\D+(.+)", infos).group(1)
        })

        for item in self.soup.select("#tabResult tr"):
            self.save_values({
                "item_cod": item.select_one(".RCod").text,
                "item_desc": item.select_one(".txtTit").text,
                "item_qtd": item.select_one(".Rqtd").contents[1],
                "item_unit": item.select_one(".RUN").contents[1],
                "item_valor": item.select_one(".RvlUnit").contents[1],
                "item_total": item.select_one(".valor").text
            })
