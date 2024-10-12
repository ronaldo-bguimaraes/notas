import os
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from src.step import Step


class Extracao(Step):
    def __init__(self, request):
        super().__init__(request)
        self.target_url = self.request["target_url"]

    def identify(self):
        pass

    def handler(self):
        session = requests.Session()
        response = session.get(self.target_url)
        buffer = response.content

        soup = BeautifulSoup(buffer, "html.parser")
        curdate = datetime.now()
        timestamp = int(curdate.timestamp())
        chave = re.sub("\\s+", "", soup.select_one("span.chave").text)

        foldename = f"/tmp/extracao"
        os.makedirs(foldename, exist_ok=True)

        filename = f"chave_{chave}_{timestamp}.html"
        filepath = Path(foldename, filename)

        with open(filepath, mode="wb") as file:
            file.write(buffer)

        return {
            "filepath": str(filepath.resolve())
        }
