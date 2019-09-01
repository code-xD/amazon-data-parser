from django import forms

country_dict = (
    ('China', 'China'),
    ('India', 'India'),
    ('Japan', 'Japan'),
    ('Singapore', 'Singapore'),
    ('Turkey', 'Turkey'),
    ('United Arab Emirates', 'United Arab Emirates'),
    ('France', 'France'),
    ('Germany', 'Germany'),
    ('Italy', 'Italy'),
    ('Netherlands',	'Netherlands'),
    ('Spain', 'Spain')	,
    ('United Kingdom',	'United Kingdom'),
    ('Canada', 'Canada'),
    ('Mexico', 'Mexico'),
    ('United States', 'United States'),
    ('Australia',	'Australia'),
    ('Brazil',	'Brazil'))

website_choice = (
    ('Amazon', 'Amazon'),
    ('Etsy', 'Etsy'),
    ('Snapdeal', 'Snapdeal'),
    ('Alibaba', 'Alibaba'),
    ('Flipkart', 'Flipkart')
)


class AmazonProductForm(forms.Form):
    Product_name = forms.CharField(max_length=100)
    Country = forms.ChoiceField(choices=country_dict)
    Category = forms.CharField(label='Category(Optional)', max_length=100, required=False)


class OtherProductForm(forms.Form):
    Product_name = forms.CharField(max_length=100)


class WebsiteForm(forms.Form):
    Website = forms.ChoiceField(choices=website_choice)
