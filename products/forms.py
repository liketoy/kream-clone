from django import forms
from products import models


class SearchForm(forms.Form):

    PRICE_CHOICES = (
        ("-100000", "10만원 이하"),
        ("100000-300000", "10만원 - 30만원 이하"),
        ("300000-500000", "30만원 - 50만원 이하"),
        ("500000-", "50만원 이상"),
    )

    keyword = forms.CharField(required=False)
    price = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=PRICE_CHOICES, required=False
    )
    brands = forms.ModelMultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        queryset=models.Brand.objects.all(),
    )
