#import requests
#from bs4 import BeautifulSoup

#url = "https://www.nytimes.com/"
#r = requests.get(url)
#htmlcontent = r.content
##print(htmlcontent)
#
#soup = BeautifulSoup(htmlcontent,'html.parser')
##print(soup.prettify)
#
#
#articles = soup.find_all('article', class_='css-8atqhb')
#
#for article in articles:
#    title = article.find('h2').get_text()
#    description = article.find('p', class_='css-1echdzn').get_text()
#    print(title, description)

#title = soup.title
#print(title)
#print(type(title))


import requests
from bs4 import BeautifulSoup


def scrape_nytimes():
    url = 'https://www.nytimes.com/'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Error:', e)
        return []

    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', class_='css-8atqhb')

    data = []
    for article in articles:
        title = article.find('h2').get_text()
        description = article.find('p', class_='css-1echdzn').get_text()
        data.append((title, description))

    return data
data = scrape_nytimes()
print(data)
