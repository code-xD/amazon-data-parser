import csv
from .forms import WebsiteForm, AmazonProductForm, OtherProductForm
from django.http import StreamingHttpResponse
from .models import Dataset
from .parser import get_amazon_data, get_etsy_data, get_alibaba_data, get_flipkart_data, get_snapdeal_data
from django.shortcuts import render, redirect
from .machinemodels import EtsyCSVwriter,AlibabaCSVwriter
from django.http import HttpResponse
import time


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def printCSV(data):
    try:
        dataset = Dataset.objects.get(
            name=data['Website'][0]+'-'+data['keyword'][0])
        rows = []
        fields = []
        # reading csv file
        with open(dataset.ml_file.path, 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            # extracting each data row one by one
            count = 0
            for row in csvreader:
                count += 1
                if count > 200:
                    break
                rows.append(row)
        return {'fields':fields,'rows':rows}
    except:
        return None            

def home(request):
    if request.method == 'POST':
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        data = dict(request.POST)
        print(data)
        if data['Website'][0] == 'Amazon':
            if data['category'][0] == '':
                response = StreamingHttpResponse((writer.writerow(data) for data in get_amazon_data(data['keyword'][0], data['Country'][0])),
                                                    content_type="text/csv")
            else:
                response = StreamingHttpResponse((writer.writerow(data) for data in get_amazon_data(data['keyword'][0], data['Country'][0], data['category'][0])),
                                                    content_type="text/csv")
            response['Content-Disposition'] = f"""attachment; filename="{data['Website']}-{data['keyword']}-{data['Country']}-{data['category']}.csv"""
            return response
        elif data['Website'][0] == 'Etsy':
            EtsyCSVwriter.delay(data['keyword'][0])
        elif data['Website'][0] == 'Alibaba':
            AlibabaCSVwriter.delay(data['keyword'][0])
        data = printCSV(data)    
        if data is None:
            return render(request, "file/index.html", {"csv": False})
        return render(request, 'file/index.html', {"csv": True,'rows': data['rows'], 'fields': data['fields']})
    return render(request, 'file/index.html', {"csv": False})


def website_form(request, website):
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    if website == 'Amazon':
        if request.method == 'POST':
            form = AmazonProductForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(data)
                if data['Category'] == '':
                    response = StreamingHttpResponse((writer.writerow(data) for data in get_amazon_data(data['Product_name'], data['Country'])),
                                                     content_type="text/csv")
                else:
                    response = StreamingHttpResponse((writer.writerow(data) for data in get_amazon_data(data['Product_name'], data['Country'], data['Category'])),
                                                     content_type="text/csv")
                response['Content-Disposition'] = f"""attachment; filename="{website}-{data['Product_name']}-{data['Country']}-{data['Category']}.csv"""
                return response
        form = AmazonProductForm()
    else:
        if request.method == 'POST':
            form = OtherProductForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if website == 'Etsy':
                    EtsyCSVwriter.delay(data['Product_name'])
                    time.sleep(10)
                    return redirect("/history")
                elif website == 'Snapdeal':
                    response = StreamingHttpResponse((writer.writerow(data) for data in get_snapdeal_data(data['Product_name'])),
                                                     content_type="text/csv")
                elif website == 'Alibaba':
                    AlibabaCSVwriter.delay(data['Product_name'])
                    time.sleep(10)
                    return redirect("/history")
                elif website == 'Flipkart':
                    response = StreamingHttpResponse((writer.writerow(data) for data in get_flipkart_data(data['Product_name'])),
                                                     content_type="text/csv")
                response['Content-Disposition'] = f"""attachment; filename="{website}-{data['Product_name']}.csv"""
                return response
        form = OtherProductForm()
    return render(request, 'file/website_form.html', {'form': form})


def retrieveHistoryView(request):
    datasets = Dataset.objects.all()
    return render(request, 'file/history.html', {'datasets': datasets})


def downloadFile(request, data_name):
    dataset = Dataset.objects.get(name=data_name)
    response = HttpResponse(dataset.ml_file, content_type='text/csv')
    response['Content-Disposition'] = f"""attachment; filename="{data_name}.csv"""
    return response



def viewCSV(request, data_name):
    dataset = Dataset.objects.get(name=data_name)
    rows = []
    fields = []
    # reading csv file
    with open(dataset.ml_file.path, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        # extracting each data row one by one
        count = 0
        for row in csvreader:
            count += 1
            if count >100:
                break
            rows.append(row)
    return render(request,'file/viewfile.html',{'rows':rows,'fields':fields})
