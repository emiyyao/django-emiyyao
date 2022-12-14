from django import forms

class DeepThoughtForm(forms.Form):
    deepthought_title = forms.CharField(label='Title', max_length=200)
    deepthought_description = forms.CharField(label='Description', max_length=1000)