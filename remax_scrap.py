from selenium import webdriver
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from datetime import date
import yagmail
import csv

#Get date and time
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

#Access the website
# url_remax = 'https://www.remax-quebec.com/fr/maison-a-vendre/montreal/resultats.rmx'
url_remax = 'https://www.remax-quebec.com/fr/triplex/montreal/resultats.rmx'
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

#Clear the price list in order to remove the unicode so we can compare it to criteria
prices_cleared = []
for price in prices:
    prices_cleared.append(price.replace(u'\xa0',u''))

#Get the index of the appartement that meet the criteria
criteria = 850000
indexes = []
for index, price in enumerate(prices_cleared):
    if float(price) <= criteria:
        indexes.append(index)

#Get email info from csv files
sender_info=[]

with open('sender.csv', newline='') as csv_file:
    csv_sender = csv.reader(csv_file, delimiter=',')
    for row in csv_sender:
        sender_info.append(row)

email_sender = sender_info[0][0]
pw_sender = sender_info[0][1]

receiver_info=[]
with open('receiver.csv', newline='') as csv_file:
    csv_receiver = csv.reader(csv_file, delimiter=',')
    for row in csv_receiver:
        receiver_info.append(row)

line_email =[]
#Send email
if not indexes:
    print('list is empty')
else:
    #Create the message body
    for index in indexes:
        line ='Date: ' + today + ' ULS: '+uls_nb[index] + ' Adress: ' + address[index] + ' Price: ' + prices_cleared[index] +'$ url: ' + links[index]
        line_email.append(line)

    subject = today + ' - Remax scrap'
    yag = yagmail.SMTP(email_sender, pw_sender)
    yag.send(to=receiver_info[0], subject=subject, contents=line_email)


