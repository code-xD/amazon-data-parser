from tkinter import *
from webscraper import write_file

country_dict = {
    'China'	: 'amazon.cn',
    'India'	: 'amazon.in',
    'Japan'	: 'amazon.co.jp',
    'Singapore'	: 'amazon.com.sg',
    'Turkey'	: 'amazon.com.tr',
    'United Arab Emirates'	: 'amazon.ae',
    'France'	: 'amazon.fr',
    'Germany'	: 'amazon.de',
    'Italy'	: 'amazon.it',
    'Netherlands':	'amazon.nl',
    'Spain':	'amazon.es'	,
    'United Kingdom':	'amazon.co.uk',
    'Canada':	'amazon.ca',
    'Mexico':	'amazon.com.mx',
    'United States':	'amazon.com',
    'Australia':	'amazon.com.au',
    'Brazil':	'amazon.com.br'
}

Org_list = ['Amazon', 'Etsy', 'Alibaba', 'Snapdeal', 'Flipkart']
country_list = [data for data, val in country_dict.items()]


def insert():
    print('function')
    write_file(product_name.get(),  Org_list.get(), product_category.get(), Country_list.get())


def create_dropdown(r, lst):
    variable = StringVar(mainframe)
    variable.set(lst[1])
    mylist = OptionMenu(mainframe, variable, *lst)
    mylist.grid(row=r, column=1, rowspan=1)
    # scrollbar.config(command=mylist.yview)
    return variable


if __name__ == "__main__":
    root = Tk()
    root.title('Web-Crawler')
    mainframe = Frame(root)
    mainframe.pack(side=TOP)
    buttonframe = Frame(root)
    buttonframe.pack(side=BOTTOM)
    Label(mainframe, text='Product Name:').grid(row=0, pady=10)
    Label(mainframe, text='Category(Optional):').grid(row=1, pady=10)
    Label(mainframe, text='Organisation:').grid(row=2, pady=10)
    Org_list = create_dropdown(2, Org_list)
    Country_lable = Label(mainframe, text='Country(Works for Amazon):').grid(row=3, pady=10)
    Country_list = create_dropdown(3, country_list)
    product_name = Entry(mainframe)
    product_name.grid(row=0, column=1, pady=10)
    product_category = Entry(mainframe)
    product_category.grid(row=1, column=1, pady=10)
    Runbutton = Button(buttonframe, text="Find Results", bg="green", command=insert)
    Runbutton.pack(side=LEFT)
    StopButton = Button(buttonframe, text="Stop Searching", bg="red", command=quit)
    StopButton.pack(side=RIGHT)
    root.mainloop()
