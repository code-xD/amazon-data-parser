
# Importing the model weights from pre-trained model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pickle
from .parser import get_etsy_data
from .models import Dataset
import csv
from django.core.files import File
from os.path import join
from django.conf import settings

view_path = join(settings.BASE_DIR, 'file', 'Regressor_model.sav')
load_lr_model = pickle.load(open(view_path, 'rb'))

poly_reg = PolynomialFeatures(degree=4)

lin_reg_2 = LinearRegression()


def outputetsylearner(dataset):
    # Inputting the dataset & cleaning it for direct use
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


def EtsyCSVwriter(Product_name):
    print(Product_name)
    dataset, created = Dataset.objects.get_or_create(name='Etsy-'+Product_name)
    print(dataset)
    path = join(settings.MEDIA_ROOT, 'scraped', f"{dataset.name}.csv")
    with open(path, 'w') as file:
        writer = csv.writer(file)
        for data in get_etsy_data(Product_name):
            writer.writerow(data)
    file = open(path)
    dataset.scraped_file = File(file)
    dataset.save()
    file.close()
    outputetsylearner(dataset)
