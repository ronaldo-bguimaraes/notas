import json
from abc import ABC, abstractmethod
from urllib.parse import urlparse, ParseResult
from urllib.request import urlopen

import chardet


class ExtractAbstract(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def run(self):
        pass


class SefazMT(ExtractAbstract):
    @staticmethod
    def test(data: ParseResult):
        result = data.netloc == "www.sefaz.mt.gov.br"
        result &= "nfce/consultanfce" in data.path
        return result

    def run(self):
        response = urlopen(self.url)
        buffer = response.read()
        result = chardet.detect(buffer)
        encoding = result["encoding"]
        html = buffer.decode(encoding)
        print()


mapper = {
    "SEFAZ_MT": SefazMT
}


def identify(data: ParseResult):
    for k, v in mapper.items():
        if v.test(data):
            return k


def extract_from_url(url: str):
    result = urlparse(url)
    name = identify(result)
    contructor = mapper.get(name)
    extract = contructor(url)
    extract.run()
