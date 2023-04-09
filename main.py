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


def scrapurl(result,realtime):
    url_content = BeautifulSoup(result.content, "html.parser")
    acc_scrap = url_content.find_all(class_= "ellipsis-short")
    price_scrap = url_content.find_all(class_="tv-price")
    time_scrap = url_content.find_all(class_="tv-time")
    close_scrap = url_content.find_all(class_="tv-close")
    var_scrap = url_content.find_all(class_="tv-change-percent")
    more_or_less_scrap = url_content.find_all(class_="tv-change-abs")
    acciones = []
    precio_acciones = []
    tiempo_acciones = []
    var_acciones = []
    close_acciones = []
    more_or_less_acciones = []

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
    for Stock, Price, Time, Var, Close, VarinPercent in zip(acciones, precio_acciones, tiempo_acciones, var_acciones, 
                                                            close_acciones, more_or_less_acciones):
        value = {"Stock":Stock, "Price":Price, "Time":Time, "+/-":Var, "Close":Close, "%":VarinPercent}
        realtime.append(value) 

def ad_to_wallet(realtime,wallet_total):
    df_acciones = pd.DataFrame(realtime)
    print(df_acciones)
    
    opcion = int(input("Qué valor del Ibex 35 has comprado?\n[Q]Para salir."))

    if opcion == "Q":
        main()
    else:
        Stock = realtime[opcion]["Stock"]
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
    

def show_tiempo_real(wallet_total,realtime):
    borrado = borrado_dep_so()
    while True:
        realtime = []
               
        os.system(borrado)
        result = urlcontent(url)          
        scrapurl(result,realtime)
        df = pd.DataFrame(realtime)
        print(df)
        if wallet_total:
            print('\n'*2)
            for x in wallet_total:
                 for y in x:   
                    if y == "Balance":
                        for price in realtime:
                            if price["Stock"] == x["Stock"]:
                                x["Balance"] = (price["Price"] *x["Qty"]) - x["AccountCharge"]


            df1 = pd.DataFrame(wallet_total)
            print(df1)
        sleep(5)


def menu_principal():
    opcion = input("Elije la opción:\n"
                   "[A]Añadir a tu cartera.\n"
                   "[B]Eliminar de tu cartera.\n"
                   "[C]Tiempo Real.\n")
    return opcion

def delete_to_wallet(wallet_total):
    walletdf = pd.DataFrame(wallet_total)
    print(walletdf)
    opcion = int(input("Que movimiento quieres eliminar?"))
    wallet_total.pop(opcion)
    print("Movimiento Eliminado")


def main():   
    while True:
        
        realtime = []
        result = urlcontent(url)
        scrapurl(result,realtime)
        opcion = menu_principal()
        if opcion == "A":
            ad_to_wallet(realtime,wallet_total)
        if opcion == "B":
            delete_to_wallet(wallet_total)
        if opcion == "C":
            show_tiempo_real(wallet_total,realtime)
                             
    

if __name__ == "__main__":
    main()