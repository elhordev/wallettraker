from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests

url = "https://www.bolsamania.com/indice/IBEX-35"
wallet_total = []


def borrado_dep_so():
    borrado = None
    if os.name == "posix":
        borrado = "clear"
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        borrado = "cls"
    return borrado


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
        price = price.contents[1].contents[0].replace("€","")
        price = price.replace(",",".")
        precio_acciones.append(float(price))

    for time in time_scrap:
        tiempo_acciones.append(time.contents[1].next)
    for var in var_scrap:
        var_acciones.append(var.contents[1].text)

    
def ad_to_wallet(acciones,wallet_total):
    df_acciones = pd.DataFrame(acciones)
    print(df_acciones)
    

    opcion = int(input("Qué valor del Ibex 35 has comprado?\n[Q]Para salir."))
    if opcion == "Q":
        main()
    else:
        Stock = acciones[opcion]
        Buyprice = float(input(f"A que precio has comprado las acciones de {Stock} ?\n"))
        Qty = int(input(f"Cuantas acciones de {Stock} has comrpado a {Buyprice}?\n"))
        Expense = float(input("Cuanto te han cobrado de gastos de compra?"))
        Index = opcion
        wallet = dict(
            Stock = Stock,
            Buyprice = Buyprice,
            Qty = Qty,
            Expense = Expense,
            Index = Index,
            AccountCharge = (Buyprice * Qty) + Expense,
            Balance = 0
        )
        print(f"Añadida la compra de {Qty} acciones de {Stock} por un cargo en cuenta de {wallet['AccountCharge']} euros.")
        wallet_total.append(wallet)
    return wallet_total
    

def show_tiempo_real(acciones,precio_acciones,tiempo_acciones,var_acciones,
                     wallet_total):
    borrado = borrado_dep_so()
    while True:
        acciones = []
        precio_acciones = []
        tiempo_acciones = []
        var_acciones = []        
        os.system(borrado)
        result = urlcontent(url)          
        scrapurl(result,acciones,precio_acciones,tiempo_acciones,var_acciones)
        df = pd.DataFrame(list(zip(acciones,precio_acciones,var_acciones,tiempo_acciones)),
                          columns=["Valor","Precio","","Hora"])
        print(df)
        if wallet_total:
            for x in wallet_total:
                 for y in x:   
                    if y == "Balance":
                        x["Balance"] = (precio_acciones[x["Index"]] * x["Qty"]) - x["AccountCharge"]


            df1 = pd.DataFrame(wallet_total)
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
        
        result = urlcontent(url)
        scrapurl(result,acciones,precio_acciones,tiempo_acciones,var_acciones)
        opcion = menu_principal()
        if opcion == "A":
            ad_to_wallet(acciones,wallet_total)
        if opcion == "B":
            print("miau")
        if opcion == "C":
            show_tiempo_real(acciones,precio_acciones,tiempo_acciones,var_acciones,wallet_total)
    

if __name__ == "__main__":
    main()