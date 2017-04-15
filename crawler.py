from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import csv
from time import sleep
import re

# specify parameters of the website page
zipcode = '94087'
url='https://www.truecar.com/used-cars-for-sale/listings/volkswagen/location-{zipcode}/?page={page}&used_opt=usedmake'

# save infomation in 'auto_info.csv'
auto_file = open('auto_info.csv','wb')
auto_writer = csv.writer(auto_file, delimiter = ',')

page = 0

while page < 10000:
    page += 1
    print 'fetch:', url.format(zipcode = zipcode, page = page)

    # fetch html
    try:
        html = requests.get(url.format(zipcode = zipcode, page = page))
    except requests.exceptions.RequestException as e:
        print e
        break

    # analyse html, save to csv
    soup = BeautifulSoup(html.text, 'html5lib')
    auto_list = soup.select('.vehicle-card')

    if not auto_list:
        break

    for auto in auto_list:
        auto_name = auto.select('.vdp-link')[1].string
        auto_price = auto.select('.price')[0].string
        mileage = auto.find(string = re.compile('mile'))
        # exterior color
        if not auto.find(string = 'Exterior'):
            exterior = 'NA'
        else:
            exterior = auto.find(string = 'Exterior').parent.parent.text
        # interior color
        if not auto.find(string = 'Interior'):
            interior = 'NA'
        else:
            interior = auto.find(string = 'Interior').parent.parent.text

        auto_writer.writerow([auto_price, auto_name, mileage, exterior, interior])


auto_file.close()
