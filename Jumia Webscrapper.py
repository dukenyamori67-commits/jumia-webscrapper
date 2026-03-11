# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 13:15:16 2026

@author: Dukem
"""

import requests
from bs4 import BeautifulSoup
import psycopg2
import time

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="jumiaphones",
    user="postgres",
    password="@4Youreyezonly"
)

cursor = conn.cursor()

base_url = "https://www.jumia.co.ke/catalog/?q=mobile+phones&page={}"

headers = {"User-Agent": "Mozilla/5.0"}

page = 1

while True:
    
    url = base_url.format(page)
    print(f"Scraping page {page}")
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    products = soup.find_all("article", class_="prd")
    
    if not products:
        print("Finished scraping.")
        break
    
    for product in products:
        
        name = product.find("h3", class_="name")
        price = product.find("div", class_="prc")
        rating = product.find("div", class_="stars")
        link = product.find("a", class_="core")
        
        name = name.text.strip() if name else None
        price = price.text.strip() if price else None
        rating = rating.text.strip() if rating else None
        
        if link:
            link = "https://www.jumia.co.ke" + link.get("href")
        
        # Insert into PostgreSQL
        cursor.execute(
            """
            INSERT INTO jumia_phones(product_name, price, rating, product_link)
            VALUES (%s, %s, %s, %s)
            """,
            (name, price, rating, link)
        )
        
        conn.commit()
    
    page += 1
    time.sleep(2)

cursor.close()
conn.close()

print("Data successfully stored in PostgreSQL.")