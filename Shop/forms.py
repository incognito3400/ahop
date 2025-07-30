from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    
    class Meta:
        model = Room
        fields = [
            'number', 'type', 'price', 'is_available', 'phone', 'address', 'rooms_count', 'size', 'floors'
        ]
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'rooms_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'class': 'form-control'}),
            'floors': forms.NumberInput(attrs={'class': 'form-control'}),
        }

