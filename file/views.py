import csv
from .forms import WebsiteForm, AmazonProductForm, OtherProductForm
from django.http import StreamingHttpResponse
from .parser import get_amazon_data, get_etsy_data, get_alibaba_data, get_flipkart_data, get_snapdeal_data
from django.shortcuts import render, redirect


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def home(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            website_dict = form.cleaned_data
            return redirect(f"/{website_dict['Website']}")
    form = WebsiteForm()
    return render(request, 'file/home.html', {'form': form})


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
                    response = StreamingHttpResponse((writer.writerow(data) for data in get_etsy_data(data['Product_name'])),
                                                     content_type="text/csv")
                elif website == 'Snapdeal':
                    response = StreamingHttpResponse((writer.writerow(data) for data in get_snapdeal_data(data['Product_name'])),
                                                     content_type="text/csv")
                elif website == 'Alibaba':
                    response = StreamingHttpResponse((writer.writerow(data) for data in get_alibaba_data(data['Product_name'])),
                                                     content_type="text/csv")
                elif website == 'Flipkart':
                    response = StreamingHttpResponse((writer.writerow(data) for data in get_flipkart_data(data['Product_name'])),
                                                     content_type="text/csv")
                response['Content-Disposition'] = f"""attachment; filename="{website}-{data['Product_name']}.csv"""
                return response
        form = OtherProductForm()
    return render(request, 'file/website_form.html', {'form': form})
