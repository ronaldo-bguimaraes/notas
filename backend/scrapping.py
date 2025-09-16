from datetime import datetime
import json
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup

def get_data(qr_code_url: str):
    session = requests.Session()
    response = session.get(qr_code_url)
    buffer = response.content

    soup = BeautifulSoup(buffer, "html.parser")
    curdate = datetime.now()

    timestamp = int(curdate.timestamp())

    data = {
        "titulo": soup.select_one("#conteudo .txtCenter .txtTopo").text,
        "chave": re.sub("\\s+", "", soup.select_one("span.chave").text),
        "scrapping_timestamp": timestamp,
    }

    items = []

    def _extract_code(data: str):
        return re.search("\\s+(\\d+)\\s", data).group(1)

    def _extract_value(data: str):
        return re.search("(\\d+(?:\\.\\d{3})*,\\d{1,2})", data).group(1)

    for item in soup.select("#tabResult tr"):
        item_values = {
            "item_codigo": _extract_code(item.select_one(".RCod").text),
            "item_descricao": item.select_one(".txtTit").text,
            "item_quantidade": item.select_one(".Rqtd").contents[1],
            "item_tipo_unidade": item.select_one(".RUN").contents[1],
            "item_valor_unidade": _extract_value(item.select_one(".RvlUnit").contents[1]),
            "item_valor_total": _extract_value(item.select_one(".valor").text)
        }
        items.append(item_values)
    
    data["items"] = items

    print(json.dumps(data, indent=4, ensure_ascii=False))

def test_run():
    qr_code_url = "https://www.sefaz.mt.gov.br/nfce/consultanfce?p=51250809477652008413651160001087671228558149|2|1|1|278155C022E96800A4ACABF2614AA8773B4551F6"
    get_data(qr_code_url)

if __name__ == "__main__":
    test_run()
