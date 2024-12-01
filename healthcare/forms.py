from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import TextInput, PasswordInput
from .models import Ugonjwa, TyphoidPhoto, Typhoid, Illness, Sign, Merchandise, Image, User

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username',
                'email', 'password1', 'password2']
        
        def save(self, commit=True): 
            user = super().save(commit=False) 
            user.first_name = self.cleaned_data['first_name'] 
            user.last_name = self.cleaned_data['last_name'] 
            user.email = self.cleaned_data['email'] 
            if commit: user.save() 
            return user

class TyphoidForm(forms.ModelForm): 
    class Meta: 
        model = Typhoid
        fields = ['disease_name', 'disease_symptoms']

class TyphoidPhotoForm(forms.ModelForm):
    class Meta:
        model=TyphoidPhoto
        fields=['photo']

TyphoidPhotoFormSet= forms.inlineformset_factory(Typhoid, TyphoidPhoto, form=TyphoidPhotoForm, extra=8)



class IllnessForm(forms.ModelForm):
    class Meta:
        model = Illness
        fields = ['name', 'description']

class SignForm(forms.ModelForm):
    class Meta:
        model = Sign
        fields = ['pic']

class SearchForm(forms.Form):
    query=forms.CharField(max_length=100, required=True)


class MerchandiseForm(forms.ModelForm):
    class Meta:
        model=Merchandise
        fields=['name', 'details']

class ImageForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=['sample', 'image']