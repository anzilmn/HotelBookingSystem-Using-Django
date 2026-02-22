from django import forms
from django.core.exceptions import ValidationError
from datetime import date

class AvailabilityForm(forms.Form):
    check_in = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    check_out = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        # 1. Check if dates are in the past
        if check_in and check_in < date.today():
            raise ValidationError("Vro, you can't book a room in the past!")

        # 2. Check if Check-out is after Check-in
        if check_in and check_out and check_out <= check_in:
            raise ValidationError("Check-out date must be after the Check-in date.")
        
        return cleaned_data



from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about your stay...'}),
        }