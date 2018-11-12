# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 18:09:55 2018

@author: iosu
"""
import requests
from bs4 import BeautifulSoup
import time
import csv

def extraer_productos(url, fecha):
    print('-------------------------------')
    print(url)
    products = [];
    page = requests.get( url )
    soup = BeautifulSoup(page.content, 'lxml')
    
    #Recorremos la lista de productos
    for ul in soup.find_all("ul", {"class": "products-list"}):
        for product in ul.find_all('div', {"class": "product-wrapper"}):
           # id = product.get('data-modelnumber')
            p = get_datos_producto(product,fecha)
            #print(id)
            products.append(p)
            
    # Si hay siguiente página, accedemos a ella y extreamos los productos
    ulPagination = soup.find('ul', {"class": "pagination"})
    liPaginationNext = ulPagination.find('li', {"class": "pagination-next"})

    if liPaginationNext != None:
        nextPage = 'https://www.mediamarkt.es' +  liPaginationNext.a['href']
        products = products + extraer_productos(nextPage,fecha)
    return products

def get_datos_producto(product,fecha):
    
    #Obtenemos el id del producto
    id = product.get('data-modelnumber')
    
    #Obtenemos el nombre el producto
    divContenido = product.find('div', {"class": "content"})
    nombre = divContenido.h2.a.string
    nombre = nombre.replace('\n', '').replace('\r', '').replace('\t', '') 
    #Obtenemos el precio
    divPrecio = product.find('div', {"class": "price-box"})
    precio = divPrecio.find('div', {"class": "price"})
    precio = precio.string.replace("-", "00")
    return [fecha,id,nombre,precio]

def generar_csv(datos,cabecera, nombreFichero):
    with open(nombreFichero, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(cabecera)
        for d in datos:
            writer.writerow(d)

cabecera = ['fecha','id','nombre','precio']
fecha = time.strftime("%d-%m-%y")
      
url = "https://www.mediamarkt.es/es/category/_smartphones-701189.html"
products = extraer_productos(url,fecha)
generar_csv(products,cabecera, fecha+'_smartphones.csv')
