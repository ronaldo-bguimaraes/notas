import json
import os
import re
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

from src.step import Step


class Parser(Step):
    def __init__(self, request):
        super().__init__(request)
        self.filepath = self.request["filepath"]
        self.soup: Optional[BeautifulSoup] = None

    def handler(self):
        with open(self.filepath, mode="rb") as file:
            buffer = file.read()

        self.soup = BeautifulSoup(buffer, "html.parser")

        result = self.parse_title()

        foldename = f"/tmp/parseado"
        os.makedirs(foldename, exist_ok=True)

        data = json.dumps(result)

        filename = Path(self.filepath).stem + "_parsed.json"
        filepath = Path(foldename, filename)

        with open(filepath, mode="w") as file:
            file.write(data)

        return {
            "filepath": str(filepath.resolve())
        }

    def parse_title(self):
        header = []
        for node in self.soup.select("#conteudo .txtCenter .text"):
            header.append(node.text)

        return {
            "title": self.soup.select_one("#conteudo .txtCenter .txtTopo").text,
            "chave": self.soup.select_one("span.chave").text,
            "complemento": header,
            "list_item": self.get_itens(),
            "infos": self.get_infos()
        }

    def get_itens(self):
        result = []
        for item in self.soup.select("#tabResult tr"):
            result.append({
                "item_cod": item.select_one(".RCod").text,
                "item_desc": item.select_one(".txtTit").text,
                "item_qtd": item.select_one(".Rqtd").contents[1],
                "item_unit": item.select_one(".RUN").contents[1],
                "item_valor": item.select_one(".RvlUnit").contents[1],
                "item_total": item.select_one(".valor").text
            })

        return result

    def get_infos(self):
        infos = self.soup.select_one("#infos").text
        return {
            "numero": re.search("N.mero\\D+(\\d+)", infos).group(1),
            "serie": re.search("S.rie\\D+(\\d+)", infos).group(1),
            "emissao": re.search("Emiss.o\\D+(.+)", infos).group(1)
        }
