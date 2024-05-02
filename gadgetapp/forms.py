from django import forms
from .models import Gadget,ProfileUser,Newsletter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CustomUserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('owner','Owner'),('user','User')])

    class Meta:
        model = ProfileUser
        fields =  ['username', 'email', 'password1', 'password2','role']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.role = self.cleaned_data['role']

            if commit:
                user.save()
            return user



class GadgetForm(forms.ModelForm):

    class Meta:

        model = Gadget
        fields = ('name','brand','price','category','image','quantity')
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'brand': forms.TextInput(attrs={'class': 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control'}),
        'category': forms.TextInput(attrs={'class': 'form-control'}),
        'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }
    

class NewsLetterForm(forms.ModelForm):

    class Meta:

        model = Newsletter
        fields = ('email',)
    

    
