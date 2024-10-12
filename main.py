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
            # "target_url": qr_code_url,
            'filepath': '/tmp/extracao/chave_51240979379491005819651180002693641903633685_1728702205.html'
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
