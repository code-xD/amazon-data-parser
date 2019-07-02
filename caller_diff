# For Flipkart
if __name__ == '__main__':
    fields = ['Product Name', 'Image URL', 'Product URL',
              'price', 'Ratings', 'No: of Responses', 'country']
    if not path.exists("E-commerce Data.csv"):
        f = open("E-commerce Data.csv", "a")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        f.close()
    with open('E-commerce Data.csv', 'a') as csvfile:
        print('data')
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        for data in get_flipkart_data("Wooden Clock"):
            writer.writerow(data)


# For Snapdeal
if __name__ == '__main__':
    fields = ['Product Name', 'Image URL', 'Product URL',
              'price', 'Ratings', 'No: of Responses', 'country']
    if not path.exists("E-commerce Data.csv"):
        f = open("E-commerce Data.csv", "a")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        f.close()
    with open('E-commerce Data.csv', 'a') as csvfile:
        print('data')
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        for data in get_snapdeal_data("Wooden Clock"):
            writer.writerow(data)


# For Alibaba
if __name__ == '__main__':
    fields = ['Product Name', 'Image URL', 'Product URL',
              'price', 'Ratings', 'No: of Responses', 'country']
    if not path.exists("E-commerce Data.csv"):
        f = open("E-commerce Data.csv", "a")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        f.close()
    with open('E-commerce Data.csv', 'a') as csvfile:
        print('data')
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        for data in get_alibaba_data('Wooden Clock'):
            writer.writerow(data)

# For Amazon ( UK )

if __name__ == '__main__':
    fields = ['Product Name', 'Image URL', 'Product URL',
              'price', 'Ratings', 'No: of Responses', 'country']
    if not path.exists("E-commerce Data.csv"):
        f = open("E-commerce Data.csv", "a")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        f.close()
    with open('E-commerce Data.csv', 'a') as csvfile:
        print('data')
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        for data in get_amazon_data('Wooden Clock', get_country_amazon('United Kingdom'), 'United Kingdom'):
            writer.writerow(data)


# For Etsy 
if __name__ == '__main__':
    fields = ['Product Name', 'Image URL', 'Product URL',
              'price', 'Ratings', 'No: of Responses', 'country']
    if not path.exists("E-commerce Data.csv"):
        f = open("E-commerce Data.csv", "a")
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        f.close()
    with open('E-commerce Data.csv', 'a') as csvfile:
        print('data')
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        for data in get_etsy_data("Wooden Clock"):
            writer.writerow(data)
