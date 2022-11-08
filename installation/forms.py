from django import forms
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from panel.models import ExtendedAuthUser
from .models import SiteModel


#new admin register form
class AdminRegisterForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:capitalize;','class':'form-control','aria-label':'first_name'}),error_messages={'required':'First is required'})
    last_name=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:capitalize;','class':'form-control','aria-label':'last_name'}),error_messages={'required':'Last name is required'})
    username=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:capitalize;','class':'form-control','aria-label':'username'}),error_messages={'required':'Username is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','aria-label':'email'}),error_messages={'required':'Email address is required'})
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':"password",'aria-label':'password1'}),error_messages={'required':'Password is required'})
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','aria-label':'password2'}),error_messages={'required':'Confirm password is required'})
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password1','password2']


    def clean_first_name(self):
        first_name=self.cleaned_data['first_name']
        if not str(first_name).isalpha():
                raise forms.ValidationError('only characters are allowed.')
        return first_name
    
    def clean_last_name(self):
        last_name=self.cleaned_data['last_name']
        if not str(last_name).isalpha():
                raise forms.ValidationError('only characters are allowed.')
        return last_name
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with this email already exists.')
        try:
            validate_email(email)
        except ValidationError as e:
            raise forms.ValidationError('Invalid email address.')
        return email

    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
                raise forms.ValidationError('A user with this username already exists.')
        return username


class ExtendedAdminRegisterForm(forms.ModelForm):
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class':'form-control','aria-label':'phone'},initial='KE'),error_messages={'required':'Phone number is required'})

    class Meta:
        model=ExtendedAuthUser
        fields=['phone']


class SiteConfigForm(forms.ModelForm):
    site_name=forms.CharField(widget=forms.TextInput(attrs={'style':'text-transform:capitalize;','class':'form-control','aria-label':'site_name'}),error_messages={'required':'Site name is required'})
    site_url=forms.URLField(widget=forms.URLInput(attrs={'style':'text-transform:lowercase;','placeholder':'eg example.com','class':'form-control','aria-label':'site_url'}),error_messages={'required':'Site url is required'})
    timezone=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','aria-label':'timezone'}),error_messages={'required':'Timezone is required'})
    main=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input','aria-label':'main','checked':True}),error_messages={'required':'This field is required'})
    class Meta:
        model=SiteModel
        fields=['site_name','site_url','main','timezone',]
