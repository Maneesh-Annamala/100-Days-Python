# from bs4 import BeautifulSoup
# import requests

# response = requests.get("https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=paracord&viewtype=&tab=&has4Tab=true")

# web_data = response.text

# soup = BeautifulSoup(web_data,"html.parser")

# class_url = soup.select("div.fy23-search-card.m-gallery-product-item-v2.J-search-card-wrapper.fy23-list-card.searchx-offer-item")

# print("fy23-search-card" in response.text)

# # print(len(class_url))

from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

url = "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=paracord&viewtype=&tab=&has4Tab=true"

driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

products = soup.find_all("div", class_="fy23-search-card")
# images = soup.select("div.search-card-e-slider__wrapper a.href")
# product_links = soup.select("h2.search-card-e-title a.href")
# titles = soup.select("h2.search-card-e-title span")
# prices = soup.select("div.search-card-e-price-main")
# # 

# reviews = soup.select("span.search-card-e-review span")


with open("products.csv","a",encoding="utf-8") as file:
    for product in products:
        title = product.select_one("h2.search-card-e-title span")
        image_link = product.select_one("div.search-card-e-slider__wrapper a[href]").get("href")
        product_link = product.select_one("h2.search-card-e-title a[href]").get("href")
        price = product.select_one("div.search-card-e-price-main")
        rating = product.select_one("span.search-card-e-review")

        prod_t = title.get_text(strip=True) if title else "No Title"
        prod_img = image_link if image_link else "No image Link"
        prod_link = product_link if product_link else "No Product Link"
        prod_price = price.get_text(strip=True) if price else "Price Not Found"
        prod_rating = rating.get_text(" ",strip=True) if rating else "No ratings"

        file.write(f"{prod_t},{prod_img},{prod_link},{prod_price},{prod_rating}\n")

print(len(products))
   

driver.quit()