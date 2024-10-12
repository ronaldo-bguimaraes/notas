import os
import re
from datetime import datetime
from pathlib import Path

import chardet
import requests
from bs4 import BeautifulSoup


class Extracao:
    def __init__(self, target_url):
        self.target_url = target_url

    def identify(self):
        pass

    def run(self):
        session = requests.Session()
        response = session.get(self.target_url)
        buffer = response.content
        result = chardet.detect(buffer)
        encoding = result["encoding"]
        html = buffer.decode(encoding).encode("utf8")

        soup = BeautifulSoup(html, "html.parser")
        curdate = datetime.now()
        timestamp = int(curdate.timestamp())
        chave = re.sub("\\s+", "", soup.select_one("span.chave").text)

        foldename = f"/tmp/notas"
        os.makedirs(foldename, exist_ok=True)

        filename = f"chave_{chave}_{timestamp}.html"
        filepath = Path(foldename, filename)

        with open(filepath, mode="wb") as file:
            file.write(html)


if __name__ == "__main__":
    extracao = Extracao(
        target_url="https://www.sefaz.mt.gov.br/nfce/consultanfce?p=51240979379491005819651180002693641903633685|2|1|1|46426C8BD6D60F32AAC7AD72A4474CA3E1A66D39"
    )
    extracao.run()
