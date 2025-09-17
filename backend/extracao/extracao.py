import requests


class Extracao:
    def __init__(self, target_url: str):
        self.target_url = target_url

    def identify(self):
        pass

    def run(self) -> bytes:
        session = requests.Session()
        response = session.get(self.target_url)
        buffer = response.content

        return buffer