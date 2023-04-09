import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.amazon.com/s?k=ps4&ref=nb_sb_noss_1"

Headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36','Accept-Language':'en-US, en;q=0.5'})

webpage = requests.get(url,headers=Headers)
#print(webpage)

#print(type(webpage.content))

soup = BeautifulSoup(webpage.content,"html.parser")

#print(soup)

links = soup.find_all("a", attrs={'class':"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
#print(links[0].get('href'))
print(len(links))
link = links[7].get('href')
product_link = "https://amazon.com"+link
print(product_link)

new_webpage = requests.get(product_link,headers=Headers)
#print(new_webpage)

new_soup = BeautifulSoup(new_webpage.content,"html.parser")
#print(new_soup)

product_name = new_soup.find("span",attrs={'id':'productTitle'}).text.strip()
#print(product_name)
price = new_soup.find("span",attrs={'id':'price_inside_buybox'}).text
#print(price)

print('the product name is : '+product_name)
print("price : "+price)