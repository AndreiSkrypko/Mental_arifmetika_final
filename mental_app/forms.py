from django import forms
from .models import Students

class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['name', 'age', 'parent_first_name', 'parent_last_name', 'parent_phone_number']  # Добавлены поля для родителя
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите возраст'}),
            'parent_first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя родителя'}),
            'parent_last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия родителя'}),
            'parent_phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон родителя'}),
        }
