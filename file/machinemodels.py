
# Importing the model weights from pre-trained model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pickle
import requests
from .parser import get_etsy_data,get_alibaba_data,get_amazon_data
from .models import Dataset
import csv
from django.core.files import File
from celery.utils.log import get_task_logger
from os.path import join
from django.conf import settings
from celery.decorators import task


poly_reg = PolynomialFeatures(degree=4)

lin_reg_2 = LinearRegression()

logger = get_task_logger(__name__)

def appendvolume(org , dataset , count):
    V = dataset.volume
    if org == 'Etsy':
        S = 0.036
    elif org == 'Alibaba':
        S = 0.02
    elif org == 'Amazon':
        S = 0.56
    vol_list = []
    for x in range(count):
        val = (V*0.4*S*1)//(2*x+4)
        if val<=5 :
            vol_list.append('0-5')
        else:
            vol_list.append(val)
    path = join(settings.MEDIA_ROOT, 'ml_final', f'{dataset.name}.csv')
    with open(dataset.ml_file.path,'r') as csvinput:
        with open(path, 'w') as csvoutput:
            writer = csv.writer(csvoutput)
            reader = csv.reader(csvinput)
            all = []
            row = next(reader)
            row.append('Volume')
            all.append(row)
            i = 1
            for row in reader:
                row.append(vol_list[i])
                all.append(row)
                i += 1
            writer.writerows(all)
    file = open(path)
    dataset.ml_file = File(file)
    dataset.save()
    file.close()

def outputlearner(dataset,count,org):
    # Inputting the dataset & cleaning it for direct use
    if org == 'Etsy':
        view_path = join(settings.BASE_DIR, 'file', 'Regressor_model_Etsy.sav')
    elif org == 'Alibaba':
        view_path = join(settings.BASE_DIR, 'file', 'Regressor_model_Alibaba.sav')
    load_lr_model = pickle.load(open(view_path, 'rb'))
    dataset_N = pd.read_csv(dataset.scraped_file.path)
    N = dataset_N.iloc[:, :].values
    # N.shape

    N = N[N[:, 4].argsort()[::-1]]

    z_N = np.delete(N, [0, 1, 2], axis=1)
    labelencoder_z_N = LabelEncoder()
    z_N[:, 3] = 1+labelencoder_z_N.fit_transform(z_N[:, 3])
    # Predicting ranks from our model & scaling ranks
    y_N = load_lr_model.predict(poly_reg.fit_transform(z_N))
    y_N = y_N.round(0)
    y_N = y_N.astype(int)
    y_N = np.interp(y_N, (y_N.min(), y_N.max()), (+1, +20))
    # Making & Sorting the final output file
    N.shape
    final = np.concatenate((N, y_N[:, None]), axis=1)
    final = final[final[:, 7].argsort()]
    # Renaming the columns in table & Saving the table into csv file
    data = pd.DataFrame(final, columns=['Item', 'Image URL', 'Item URL',
                                        'Rating', 'Reviews', 'Price', 'Country', 'Predicted Rank'])
    path = join(settings.MEDIA_ROOT, 'machinelearned', f'{dataset.name}.csv')
    pd.DataFrame(data).to_csv(path)
    file = open(path)
    dataset.ml_file = File(file)
    dataset.save()
    file.close()
    appendvolume(org,dataset,count)



@task(name="machinelearnetsy")
def EtsyCSVwriter(Product_name):
    print(Product_name)
    dataset, created = Dataset.objects.get_or_create(name='Etsy-'+Product_name)
    params = {
    	"app_key":"975d166e40fb85507efb25df1feda61d",
    	"app_id":"b5c9ae7c",
    	"seeds": Product_name,
    	"engine":"google",
    	"country_code":"US",
    	"scale":"True",
    	"sort":"total"
    }
    r = requests.post('https://api.lc.wordtracker.com/v2/fetch', params = params)
    try:
        volume = int(r.json()['results'][0]["avg_volume_for_last_12_months"])
    except:
        volume = 0    
    dataset.volume = volume
    dataset.save()
    print(volume)
    count =  0
    path = join(settings.MEDIA_ROOT, 'scraped', f"{dataset.name}.csv")
    with open(path, 'w') as file:
        writer = csv.writer(file)
        for data in get_etsy_data(Product_name):
            count+=1
            writer.writerow(data)
    f = open(path)
    dataset.scraped_file = File(f)
    dataset.save()
    f.close()
    outputlearner(dataset,count,'Etsy')

@task(name="machinelearnalibaba")
def AlibabaCSVwriter(Product_name):
    print(Product_name)
    dataset, created = Dataset.objects.get_or_create(name='Alibaba-'+Product_name)
    params = {
    	"app_key":"975d166e40fb85507efb25df1feda61d",
    	"app_id":"b5c9ae7c",
    	"seeds": Product_name,
    	"engine":"google",
    	"country_code":"US",
    	"scale":"True",
    	"sort":"total"
    }
    r = requests.post('https://api.lc.wordtracker.com/v2/fetch', params = params)
    try:
        volume = int(r.json()['results'][0]["avg_volume_for_last_12_months"])
    except:
        volume = 0
    dataset.volume = volume
    dataset.save()
    print(volume)
    count =  0
    path = join(settings.MEDIA_ROOT, 'scraped', f"{dataset.name}.csv")
    with open(path, 'w') as file:
        writer = csv.writer(file)
        for data in get_alibaba_data(Product_name):
            count+=1
            writer.writerow(data)
    f = open(path)
    dataset.scraped_file = File(f)
    dataset.save()
    f.close()
    outputlearner(dataset,count,'Alibaba')

@task(name="machinelearnalibaba")
def AmazonCSVwriter(Product_name ,Country ,Category=None):
    print(Product_name)
    if Category is not None:
        dataset, created = Dataset.objects.get_or_create(name='Amazon-'+Product_name+'-'+Country+'-'+Category)

    else:
        dataset, created = Dataset.objects.get_or_create(
            name='Amazon-'+Product_name+'-'+Country)
    params = {
    	"app_key":"975d166e40fb85507efb25df1feda61d",
    	"app_id":"b5c9ae7c",
    	"seeds": Product_name,
    	"engine":"google",
    	"country_code":"US",
    	"scale":"True",
    	"sort":"total"
    }
    r = requests.post('https://api.lc.wordtracker.com/v2/fetch', params = params)
    try:
        volume = int(r.json()['results'][0]["avg_volume_for_last_12_months"])
    except:
        volume = 0
    dataset.volume = volume
    dataset.save()
    print(volume)
    count =  0
    path = join(settings.MEDIA_ROOT, 'scraped', f"{dataset.name}.csv")
    with open(path, 'w') as file:
        writer = csv.writer(file)
        for data in get_amazon_data(Product_name,Country,Category):
            count+=1
            writer.writerow(data)
    f = open(path)
    dataset.scraped_file = File(f)
    dataset.save()
    f.close()
    outputlearner(dataset,count,'Amazon')
