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
precio_valor_en_wallet = []
valor_en_wallet = []
url = "https://www.bolsamania.com/indice/IBEX-35"


def urlcontent(url):
    result = requests.get(url)
    return result


def scrapurl(result,acciones,precio_acciones,tiempo_acciones,var_acciones):
    url_content = BeautifulSoup(result.content, "html.parser")
    acc_scrap = url_content.find_all(class_= "text-left ficha-name")
    price_scrap = url_content.find_all(class_= "text-right ficha-price")
    time_scrap = url_content.find_all(class_= "text-right ficha-time")
    var_scrap = url_content.find_all(class_= "text-right ficha-var-por")

    for acc in acc_scrap:
        acciones.append(acc.contents[1].next)
    for price in price_scrap:
        precio_acciones.append(price.contents[1].next)
    for time in time_scrap:
        tiempo_acciones.append(time.contents[1].next)
    for var in var_scrap:
        var_acciones.append(var.contents[1].text)
    
    
def ad_to_wallet(acciones,valor_en_wallet,precio_valor_en_wallet):
    df_acciones = pd.DataFrame(acciones)
    print(df_acciones)

    opcion = int(input("Qué valor del Ibex 35 has comprado?\n[Q]Para salir."))
    if opcion == "Q":
        main()
    else:
        valor_en_wallet.append(acciones[opcion])
        opcion1 = float(input("A qué precio has comprado?"))
        precio_valor_en_wallet.append(opcion1)
        numero_de_acciones = int(input("Cuantas acciones has comprado?"))
        opcion2 = float(input("Cuánto te han cobrado en gastos de compra?"))
        neto_en_cuenta = (opcion1 * numero_de_acciones - opcion2)
        print(f"Añadida la Compra de {opcion1} acciones del {acciones[opcion]} por un valor de cargo en cuenta de {neto_en_cuenta}€.")
        
    return valor_en_wallet
    

def show_tiempo_real(acciones,precio_acciones,tiempo_acciones,var_acciones,valor_en_wallet,precio_valor_en_wallet):
    while True:
        acciones = []
        precio_acciones = []
        tiempo_acciones = []
        var_acciones = []
        
        os.system(borrado)
        result = urlcontent(url)          
        scrapurl(result,acciones,precio_acciones,tiempo_acciones,var_acciones)
        df = pd.DataFrame(list(zip(acciones,precio_acciones,var_acciones,tiempo_acciones)),columns=["Valor","Precio","","Hora"])
        print(df)
        if valor_en_wallet:
            df1 = pd.DataFrame(valor_en_wallet)
            print(df1)
        sleep(5)


def menu_principal():
    opcion = input("Elije la opción:\n"
                   "[A]Añadir a tu cartera.\n"
                   "[B]Eliminar de tu cartera.\n"
                   "[C]Tiempo Real.\n")
    return opcion


def main():   
    while True:
        acciones = []
        precio_acciones = []
        tiempo_acciones = []
        var_acciones = []
        precio_valor_en_wallet = []
        result = urlcontent(url)
        scrapurl(result,acciones,precio_acciones,tiempo_acciones,var_acciones)
        opcion = menu_principal()
        if opcion == "A":
            ad_to_wallet(acciones,valor_en_wallet,precio_valor_en_wallet)
        if opcion == "B":
            print("miau")
        if opcion == "C":
            show_tiempo_real(acciones,precio_acciones,tiempo_acciones,var_acciones,valor_en_wallet,precio_valor_en_wallet)
    

if __name__ == "__main__":
    main()