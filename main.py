from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests

url = "https://www.productoscotizados.com/mercado/ibex-35"
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


def scrapurl(result,acciones,precio_acciones,tiempo_acciones,var_acciones,close_acciones,more_or_less_acciones):
    url_content = BeautifulSoup(result.content, "html.parser")
    acc_scrap = url_content.find_all(class_= "ellipsis-short")
    price_scrap = url_content.find_all(class_="tv-price")
    time_scrap = url_content.find_all(class_="tv-time")
    close_scrap = url_content.find_all(class_="tv-close")
    var_scrap = url_content.find_all(class_="tv-change-percent")
    more_or_less_scrap = url_content.find_all(class_="tv-change-abs")

    for acc in acc_scrap:
        acc = acc.text.replace("\t","").replace("\r","").replace("\n","")
        acciones.append(acc)
    for price in price_scrap:
        if "\nPrecio\n" not in price.text:
            price = price.text.replace("\n","").replace(",",".")
            precio_acciones.append(float(price))
    for time in time_scrap:
        if "\nÚLTIMA ACTUALIZACIÓN\n" not in time.text:
            time = time.text.replace("\n","")
            tiempo_acciones.append(time)
    for var in var_scrap:
        if "\n%\n" not in var.text:
            var = var.text.replace("\n","")
            var_acciones.append(var) 
    for close in close_scrap:
        if "\nPRECIO DE CIERRE\n" not in close.text:
            close = close.text.replace("\n","").replace("\t","").replace("\r","")
            close_acciones.append(close)
    for more_or_less in more_or_less_scrap:
        if "\n+/-" not in more_or_less.text:
            more_or_less = more_or_less.text.replace("\n","")
            more_or_less_acciones.append(more_or_less)

    
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
                     wallet_total,close_acciones,more_or_less_acciones):
    borrado = borrado_dep_so()
    while True:
        acciones = []
        precio_acciones = []
        tiempo_acciones = []
        var_acciones = [] 
        close_acciones = []
        more_or_less_acciones = []       
        os.system(borrado)
        result = urlcontent(url)          
        scrapurl(result,acciones,precio_acciones,tiempo_acciones,var_acciones,close_acciones,more_or_less_acciones)
        df = pd.DataFrame(list(zip(acciones,precio_acciones,close_acciones,
                                   more_or_less_acciones,var_acciones,tiempo_acciones)),
                          columns=["Stock","Price","Close Price","+/-","%","Time"])
        print(df)
        if wallet_total:
            print('\n'*2)
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
        close_acciones = []
        more_or_less_acciones = []
        result = urlcontent(url)
        scrapurl(result,acciones,precio_acciones,tiempo_acciones,var_acciones,
                 close_acciones,more_or_less_acciones)
        opcion = menu_principal()
        if opcion == "A":
            ad_to_wallet(acciones,wallet_total)
        if opcion == "B":
            print("miau")
        if opcion == "C":
            show_tiempo_real(acciones,precio_acciones,tiempo_acciones,var_acciones,wallet_total,
                             close_acciones,more_or_less_acciones)
    

if __name__ == "__main__":
    main()