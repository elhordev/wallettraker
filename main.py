from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
borrado = None
if os.name == "posix":
    borrado = "clear"
elif os.name == "ce" or os.name == "nt" or os.name == "dos":
    borrado = "cls"


url = "https://www.bolsamania.com/indice/IBEX-35"

while True:
    os.system(borrado)
    result = requests.get(url)
    url_content = BeautifulSoup(result.content, "html.parser")
    acc_scrap = url_content.find_all(class_= "text-left ficha-name")
    price_scrap = url_content.find_all(class_= "text-right ficha-price")
    time_scrap = url_content.find_all(class_= "text-right ficha-time")
    var_scrap = url_content.find_all(class_= "text-right ficha-var-por")
    acciones = []
    precio_acciones = []
    tiempo_acciones = []
    var_acciones = []

    for acc in acc_scrap:
        acciones.append(acc.contents[1].next)
    for price in price_scrap:
        precio_acciones.append(price.contents[1].next)
    for time in time_scrap:
        tiempo_acciones.append(time.contents[1].next)
    for var in var_scrap:
        var_acciones.append(var.contents[1].text)

    df = pd.DataFrame(precio_acciones,acciones)
    print(df)
   
    print(acciones[9],precio_acciones[9],tiempo_acciones[9],var_acciones[9])
    

    sleep(5451214)
    

