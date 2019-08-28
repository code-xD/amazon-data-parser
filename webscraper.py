import csv
from os import path
from parser import get_amazon_data, get_alibaba_data, get_etsy_data, get_flipkart_data, get_snapdeal_data


def write_file(product, org, category=None, country=None):
    if product == '':
        pass
    else:
        if org == 'Amazon':
            filename = org+product+country+category+'.csv'
        else:
            filename = org+product+category+'.csv'
        writedict = 1
        if path.exists('data/'+filename):
            writedict = 0
        with open('data/'+filename, 'a') as csvfile:
            print('data')
            count = 0

            if org == 'Amazon':
                print('1')
                for data in get_amazon_data(product, country, category):
                    writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()))
                    if writedict:
                        writedict = 0
                        writer.writeheader()
                    writer.writerow(data)

            elif org == 'Flipkart':
                for data in get_flipkart_data(product):
                    writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()))
                    if writedict:
                        writedict = 0
                        writer.writeheader()
                    writer.writerow(data)

            elif org == 'Snapdeal':
                for data in get_snapdeal_data(product):
                    writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()))
                    if writedict:
                        writedict = 0
                        writer.writeheader()
                    writer.writerow(data)

            elif org == 'Etsy':
                for data in get_etsy_data(product):
                    writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()))
                    if writedict:
                        writedict = 0
                        writer.writeheader()
                    writer.writerow(data)

            elif org == 'Alibaba':
                for data in get_alibaba_data(product):
                    writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()))
                    if writedict:
                        writedict = 0
                        writer.writeheader()
                    writer.writerow(data)
