import csv
from os import path
from parser import get_amazon_data

if __name__ == '__main__':
    extrawrite = 0
    if not path.exists("E-commerce Data.csv"):
        extrawrite = 1
    with open('E-commerce Data.csv', 'a') as csvfile:
        print('data')
        count = 0
        for data in get_amazon_data('ps4', 'United States'):
            if extrawrite == 1:
                writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()))
                writer.writeheader()
                extrawrite = 0
            if count == 0:
                writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()))
                count += 1
            writer.writerow(data)
