import re

from bs4 import BeautifulSoup

from parser.model.item import Item, Nota


class Parser:
    def __init__(self, html_bytes: bytes):
        self.html_bytes = html_bytes

    def _extract_code(self, data: str):
        return re.search("\\s+(\\d+)\\s", data).group(1)

    def _extract_value(self, data: str):
        return re.search("(\\d+(?:\\.\\d{3})*,\\d{1,2})", data).group(1)

    def run(self) -> Nota:
        soup = BeautifulSoup(self.html_bytes, "html.parser")

        infos = soup.select_one("#infos").text

        nota = Nota(
            empresa=soup.select_one("#conteudo .txtCenter .txtTopo").text,
            chave=soup.select_one("span.chave").text,
            numero=re.search("N.mero\\D+(\\d+)", infos).group(1),
            serie=re.search("S.rie\\D+(\\d+)", infos).group(1),
            emissao=re.search("Emiss.o\\D+(.+)", infos).group(1)
        )

        for item in soup.select("#tabResult tr"):
            parsed_item = Item(
                item_codigo=self._extract_code(item.select_one(".RCod").text),
                item_descricao=item.select_one(".txtTit").text,
                item_quantidade=item.select_one(".Rqtd").contents[1],
                item_tipo_unidade=item.select_one(".RUN").contents[1],
                item_valor_unidade=self._extract_value(item.select_one(".RvlUnit").contents[1]),
                item_valor_total=self._extract_value(item.select_one(".valor").text)
            )
            nota.add_item(parsed_item)

        return nota
