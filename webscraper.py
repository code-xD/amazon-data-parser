import csv
from os import path
from parser import get_amazon_data, get_amazon_ranking
import threading

extrawrite = 0


def modified_ranking():
    data = get_amazon_ranking()
    in_file = open("E-commerce Data.csv", "r")
    reader = csv.DictReader(in_file, fieldnames=list(data.keys()))
    out_file = open("E-commerce Data.csv", "w")
    writer = csv.DictWriter(out_file, fieldnames=list(data.keys()))
    count = 0
    for row in reader:
        if count == 0:
            count += 1
            continue
        row['rank list'] = data
        row['no of categories'] = len(data)
        writer.writerow(row)
    in_file.close()
    out_file.close()


def write_file(product, country):
    global extrawrite
    with open('E-commerce Data.csv', 'a') as csvfile:
        print('data')
        count = 0
        for data in get_amazon_data(product, country):
            if extrawrite == 1:
                writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()))
                writer.writeheader()
                extrawrite = 0
            if count == 0:
                writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()))
                count += 1
            writer.writerow(data)


if __name__ == '__main__':
    extrawrite = 0
    if not path.exists("E-commerce Data.csv"):
        extrawrite = 1
    # t1 = threading.Thread(target=modified_ranking)
    # t2 = threading.Thread(target=write_file,  args=('ps4', 'United States'))
    # t1.start()
    # t2.start()
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
