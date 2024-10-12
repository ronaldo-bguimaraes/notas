import re

from bs4 import BeautifulSoup

from src.step import Step


class Parser(Step):
    def __init__(self, request):
        super().__init__(request)
        self.filepath = self.request["filepath"]

    def handler(self):
        with open(self.filepath, mode="rb") as file:
            filebytes = file.read()

        html = filebytes.decode("utf8")
        soup = BeautifulSoup(html, "html.parser")

        item_list = []
        for result in soup.select("#tabResult tr"):
            item = {
                "item_cod": result.select_one(".RCod").text,
                "item_desc": result.select_one(".txtTit").text,
                "item_qtd": result.select_one(".Rqtd").contents[1],
                "item_unit": result.select_one(".RUN").contents[1],
                "item_valor": result.select_one(".RvlUnit").contents[1],
                "item_total": result.select_one(".valor").text
            }
            item_list.append(item)

        print()
