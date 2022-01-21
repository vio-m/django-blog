from .models import Rating
from django import forms


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('title', 'review', 'rating')


class CouponForm(forms.Form):
    code = forms.CharField()
