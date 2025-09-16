from extracao.extracao import Extracao
from padronizador.padronizador import Padronizador
from parser.parser import Parser


class Main:
    def __init__(self, target_url):
        self.target_url = target_url

    def run(self):
        extracao = Extracao(self.target_url)
        html_bytes = extracao.run()

        parser = Parser(html_bytes)
        result = parser.run()

        print()

qr_code_url = "https://www.sefaz.mt.gov.br/nfce/consultanfce?p=51250809477652008413651160001087671228558149|2|1|1|278155C022E96800A4ACABF2614AA8773B4551F6"

if __name__ == "__main__":
    main = Main(qr_code_url)
    main.run()
