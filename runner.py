from os import path
from parser import get_amazon_data, get_etsy_data, get_alibaba_data, get_flipkart_data, get_snapdeal_data
import csv

if __name__ == '__main__':
    fields = ['Product Name', 'Image URL', 'Product URL',
              'price', 'Ratings', 'No: of Responses', 'country', 'remark', 'rank list', 'no of categories']
    if not path.exists("E-commerce Data.csv"):
        f = open("E-commerce Data.csv", "a")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        f.close()
    with open('E-commerce Data.csv', 'a') as csvfile:
        print('data')
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        # modify the line 17 according to the site for which you want to parse the data.
        for data in get_amazon_data("carving knife",  'United States'):
            writer.writerow(data)
