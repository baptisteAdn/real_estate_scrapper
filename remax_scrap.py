from selenium import webdriver
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from datetime import date
today = date.today()
today = today.strftime('%d_%m_%Y')
import pandas as pd

#Set the path to the chrome drive
driver = webdriver.Chrome()

#Setup the arrays for parameters
uls_nb = []
address = []
prices = []
bedrooms = []
bathrooms = []
links = []

#Setup my csv file
file_name = today+"_remax.csv"
f = open(file_name, 'w')

headers = 'Date, ULS, Address, Price, Bedrooms, Bathrooms, Link\n'
f.write(headers)

#Access the website
url_remax = 'https://www.remax-quebec.com/fr/maison-a-vendre/montreal/resultats.rmx'
url_remax_root = 'https://www.remax-quebec.com'
# driver.get(url_remax)
# test=driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/div/div/div[1]/a[2]/div[2]/h2').text()

uClient = uReq(url_remax)
page_html = uClient.read()
uClient.close()

#html parsing
page_soup = soup(page_html, 'html.parser')

containers = page_soup.findAll('div',{'class':'property-entry'})

for container in containers:
    #Get the usl_nb from
    container_sub=container.findAll('a',{'class':'property-details'})
    uls=container_sub[0].div.div.get_text()
    uls = uls.split(' ')
    uls = uls[17].split('\r')
    uls = uls[0]
    uls_nb.append(uls)

    #Get the adress
    container_sub = container_sub[0].findAll('div', {'class': 'property-address'})
    address_uni = container_sub[0].h2.get_text()
    address_uni = address_uni.split('\t')
    address_uni=address_uni[2].split('\r')
    address_uni=address_uni[0]
    address.append(address_uni)

    #Get the price
    container_sub = container.findAll('a',{'class':'property-details'})
    container_sub = container_sub[0].findAll('div', {'class': 'property-details-footer'})
    container_sub = container_sub[0].findAll('div', {'class': 'property-price'})
    price = container_sub[0].get_text()
    price=price.split(' ')
    price = price[16]
    prices.append(price)

    # Get the bedrooms
    container_sub = container.findAll('a', {'class': 'property-details'})
    container_sub = container_sub[0].findAll('div', {'class': 'property-details-footer'})
    container_sub = container_sub[0].findAll('div', {'class': 'property-options'})
    container_sub = container_sub[0].span
    bedroom = container_sub.find_next_sibling('span').get_text()
    bedrooms.append(bedroom)


    #Get the bathrooms
    container_sub = container.findAll('a', {'class': 'property-details'})
    container_sub = container_sub[0].findAll('div', {'class': 'property-details-footer'})
    container_sub = container_sub[0].findAll('div', {'class': 'property-options'})
    bathroom = container_sub[0].span.get_text()
    bathrooms.append(bathroom)

    #Get the link
    link = container.a['href']
    link = url_remax_root+link
    links.append(link)

    f.write(today + ',' + uls + ',' + address_uni.replace(',',' ') + ',' + price + ',' + bedroom + ',' + bathroom + ',' + link+'\n')

f.close()




