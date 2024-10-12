# from pathlib import Path
# from urllib.parse import urlparse, parse_qs
# from urllib.request import urlopen
#
# import pandas as pd
# from bs4 import BeautifulSoup
from urllib.request import urlopen

from src.extract import extract_from_url

# import requests
# from src.files import Files

qr_code_url = "https://www.sefaz.mt.gov.br/nfce/consultanfce?p=51240979379491005819651180002693641903633685|2|1|1|46426C8BD6D60F32AAC7AD72A4474CA3E1A66D39"

extract_from_url(qr_code_url)


# tmp = Path("tmp")
# tmp.mkdir(exist_ok=True)
# 
# soup = BeautifulSoup(html, "html.parser")
# 
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
