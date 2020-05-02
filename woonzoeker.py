import requests
import os
from bs4 import BeautifulSoup
from emailhelper import CreateBodyFooter,CreateBodyHeader,CreateBodyLine,SendEmail
from dbhelper import CreateDBConnection,CloseDBConnection,InsertEntry,SelectAllEntries,SelectOneEntry
from config import *

def FormatUrls(number_of_rooms,city,min_price,max_price):
    ## If the city is not specified the function returns -1 indicating it can't continue.
    ## number_of_rooms:
    # ""  = any amount
    # 1-aantalkamers
    # 2-aantalkamers
    # 3-aantalkamers
    # 4-aantalkamers
    # 5-aantalkamers
    ## area
    # "string" -> "breda"
    ## min_price
    # 700-XXXX
    ## max_price
    # XXXX-1000
    if not city:
        return -1
    if not min_price and not max_price:
        priceurl_pararius = ""
    else:
        if min_price and not max_price:
            priceurl_pararius = min_price + "-60000/"
        else:
            if not min_price and max_price:
                priceurl_pararius = "0-" + max_price + "/"
            else:
                priceurl_pararius = min_price + "-" + max_price + "/"
    if not number_of_rooms:
        room_pararius = ""
    elif number_of_rooms == "1":
        room_pararius = "1-aantalkamers"
    elif number_of_rooms == "2":
        room_pararius = "2-aantalkamers"
    elif number_of_rooms == "3":
        room_pararius = "3-aantalkamers"
    elif number_of_rooms == "4":
        room_pararius = "4-aantalkamers"
    elif number_of_rooms == "5":
        room_pararius = "5-aantalkamers"
    pararius_url = 'https://www.pararius.nl/huurwoningen/' + city + '/' + priceurl_pararius + room_pararius
    return pararius_url

EmailBody += CreateBodyHeader(body=EmailBody)
pararius_url = FormatUrls(number_of_rooms = number_of_rooms, city = area, min_price = min_price, max_price = max_price )
pararius_response = requests.get(pararius_url)
parariusSoup = BeautifulSoup(pararius_response.content, 'html.parser')
listings_pararius = parariusSoup.find_all('li', class_='search-list__item search-list__item--listing')
for listing in listings_pararius:
    name = listing.find('h2', class_='listing-search-item__title')
    name = name.find('a', class_='listing-search-item__link listing-search-item__link--title')
    name = name.text.strip()
    location = listing.find('div', class_='listing-search-item__location')
    location = location.text.strip()
    price = listing.find('div', class_='listing-search-item__price-status')
    price = price.find('span', class_='listing-search-item__price')
    price = price.text.strip()
    link = listing.find('div', class_='listing-search-item__depiction')
    link = link.find('a', class_='listing-search-item__link listing-search-item__link--depiction')['href']
    link = 'https://www.pararius.nl' + link
    if not SelectOneEntry(dbFileName=dbFileName,entryLink=link):
        sendEmailFlag = True
        InsertEntry(dbFileName=dbFileName,entryName=name,entryLocation=location,entryPrice=price,entryLink=link)
        EmailBody += CreateBodyLine(body=EmailBody,provider='pararius',entryName=name,entryLocation=location,entryPrice=price,entryLink=link)
EmailBody += CreateBodyFooter(body=EmailBody)
if sendEmailFlag:
    SendEmail(mailUser=mailUser,mailPassword=mailPassword,mailReceiver=mailReceiver,mailSubject=mailSubject,mailBody=EmailBody)