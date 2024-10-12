from extracao.extracao import Extracao
from parser.parser import Parser

qr_code_url = "https://www.sefaz.mt.gov.br/nfce/consultanfce?p=51240979379491005819651180002693641903633685|2|1|1|46426C8BD6D60F32AAC7AD72A4474CA3E1A66D39"


class Main:
    def __init__(self, target_url):
        self.target_url = target_url

    def get_steps(self):
        return [
            {
                "name": "Realiza Parsing",
                "constructor": Parser
            }
        ]

    def run(self):
        steps = self.get_steps()
        last_response = {
            'filepath': '/tmp/notas/chave_51240979379491005819651180002693641903633685_1728698588.html'
        }
        for index, step in enumerate(steps):
            step_name = step["name"]
            constructor = step["constructor"]
            print(f"Iniciando etapa: {step_name}")
            step_object = constructor.__call__(last_response)
            last_response = step_object.handler()
            print(f"Fim da etapa: {step_name}")
            step["response"] = last_response
            print(last_response)


main = Main(qr_code_url)
main.run()

# print()
#
# # with open("tmp/tmp.html", mode="w") as tmp:
# #     tmp.write(html)
# 
# item_list = []
# for result in soup.select("#tabResult tr"):
#     item = {
#         "item_cod": result.select_one(".RCod").text,
#         "item_desc": result.select_one(".txtTit").text,
#         "item_qtd": result.select_one(".Rqtd").contents[1],
#         "item_unit": result.select_one(".RUN").contents[1],
#         "item_valor": result.select_one(".RvlUnit").contents[1],
#         "item_total": result.select_one(".valor").text
#     }
#     item_list.append(item)
# 
# df = pd.DataFrame.from_records(item_list)
# print()
