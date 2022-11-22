from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import *
from .forms import *
from django import forms
import datetime
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.forms import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.hashers import check_password
from django.core.validators import FileExtensionValidator,URLValidator
from installation.forms import SiteModel
from django.contrib.auth import authenticate
import re
from urllib.parse import urlparse
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'aria-required':'true','class':'form-control','placeholder':'Username ','aria-label':'username'}),error_messages={'required':'Username  is required'})
    password=forms.CharField(widget=forms.PasswordInput(attrs={'aria-required':'true','class':'form-control login-password','placeholder':'Password','aria-label':'password'}),error_messages={'required':'Password is required'})

    class Meta:
        model=User
        fields=['username','password',]

    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            return username
        else:
            raise forms.ValidationError('invalid username')

class UserResetPassword(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email address'}),error_messages={'required':'Email address is required'})

    def clean_email(self):
        email=self.cleaned_data['email']
        if  not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address does not exist')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('Invalid email address')
        return email

#profileForm
class CurrentLoggedInUserProfileChangeForm(UserChangeForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded'}),required=False)
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'last_name'}),error_messages={'required':'Last name is required'})
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','placeholder':'Username ','aria-label':'username'}),error_messages={'required':'Username is required'})
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control input-rounded','aria-label':'email'}),error_messages={'required':'Email address is required'})
    is_active=forms.BooleanField(widget=forms.CheckboxInput(attrs={'aria-label':'is_active','id':'checkbox1'}),required=False)
    class Meta:
        model=User
        fields=['first_name','last_name','email','is_active','username',]


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
        if email != self.instance.email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with this email already exists.')
            try:
                validate_email(email)
            except ValidationError as e:
                raise forms.ValidationError('Invalid email address.')
            return email
        else:
           return email

    def clean_username(self):
        username=self.cleaned_data['username']
        if username != self.instance.username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('A user with this username already exists')
            return username
        return username

# admin profileForm
class CurrentAdminExtUserProfileChangeForm(forms.ModelForm):
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class':'form-control input-rounded','type':'tel','aria-label':'phone','placeholder':'Phone example +25479626...'}),error_messages={'required':'Phone number is required'})
    bio=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','aria-label':'email'}),required=False)
    nickname=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'nickname'}),error_messages={'required':'Nickname is required'})
    company=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'company'}),required=False)
    timezone=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'timezone'}))
    zipcode=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'zipcode'}))
    city=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'city'}),required=False)
    country=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control input-rounded','aria-label':'country'}),required=False)
    gender=forms.ChoiceField(choices=options, error_messages={'required':'Gender is required','aria-label':'gender'},widget=forms.Select(attrs={'class':'form-control show-tick ms select2','placeholder':'Gender'}))
    birthday=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','aria-label':'birthday','type':'date'}),error_messages={'required':'Birthday is required'})   
    profile_pic=forms.ImageField(
                                widget=forms.FileInput(attrs={'class':'profile','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','gif'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=ExtendedAuthUser
        fields=['zipcode','timezone','phone','profile_pic','bio','nickname','birthday','gender','company','country','city',]

    
    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if phone != self.instance.phone:
            if ExtendedAuthUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('A user with this phone number already exists.')
            else:
                return phone
        else:
           return phone 

class UserPasswordChangeForm(UserCreationForm):
    oldpassword=forms.CharField(widget=forms.PasswordInput(attrs={'aria-required':'true','class':'form-control input-rounded','placeholder':'Old password','aria-label':'oldpassword'}),error_messages={'required':'Old password is required','min_length':'enter atleast 6 characters long'})
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'aria-required':'true','class':'form-control input-rounded','placeholder':'New password Eg Example12','aria-label':'password1'}),error_messages={'required':'New password is required','min_length':'enter atleast 6 characters long'})
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'aria-required':'true','class':'form-control input-rounded','placeholder':'Confirm new password','aria-label':'password2'}),error_messages={'required':'Confirm new password is required'})

    class Meta:
        model=User
        fields=['password1','password2']
    
    def clean_oldpassword(self):
        oldpassword=self.cleaned_data['oldpassword']
        if not self.instance.check_password(oldpassword):
            raise forms.ValidationError('Wrong old password.')
        else:
           return oldpassword

class ProfilePicForm(forms.ModelForm):
    profile_pic=forms.ImageField(
                                widget=forms.FileInput(attrs={'class':'profile','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','gif'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=ExtendedAuthUser
        fields=['profile_pic',]

#social form
class UserSocialForm(forms.ModelForm):
    facebook=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'facebook','class':'form-control input-rounded','placeholder':'Facebook Link'}),required=False)    
    twitter=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'twitter','class':'form-control input-rounded','placeholder':'Twitter Link'}),required=False)    
    instagram=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'instagram','class':'form-control input-rounded','placeholder':'Instagram Link'}),required=False)    
    linkedin=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'linkedin','class':'form-control input-rounded','placeholder':'Linkedin Link'}),required=False)   
    class Meta:
        model=ExtendedAuthUser
        fields=['facebook','twitter','linkedin','instagram',]

    def clean_facebook(self):
        facebook=self.cleaned_data['facebook']
        if URLValidator(facebook):
                output=urlparse(facebook)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [facebook,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_twitter(self):
        twitter=self.cleaned_data['twitter']
        if URLValidator(twitter):
                output=urlparse(twitter)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [twitter,username]
        else:
            raise forms.ValidationError('Invalid url')
    

    def clean_instagram(self):
        instagram=self.cleaned_data['instagram']
        if URLValidator(instagram):
                output=urlparse(instagram)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [instagram,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_linkedin(self):
        linkedin=self.cleaned_data['linkedin']
        if URLValidator(linkedin):
                output=urlparse(linkedin)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [linkedin,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_youtube(self):
        youtube=self.cleaned_data['youtube']
        if URLValidator(youtube):
                output=urlparse(youtube)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Channel id parameter missing')
                else:
                    return [youtube,username]
        else:
            raise forms.ValidationError('Invalid url')
    def clean_whatsapp(self):
        whatsapp=self.cleaned_data['whatsapp']
        if URLValidator(whatsapp):
            output=urlparse(whatsapp)
            username=output.path.strip('/')
            if not username:
                raise forms.ValidationError('username parameter missing')
            else:
                return [whatsapp,username]
        else:
            raise forms.ValidationError('Invalid url')

class SiteForm(forms.ModelForm):
    site_name=forms.CharField(widget=forms.EmailInput(attrs={'aria-label':'site_name','class':'form-control input-rounded','placeholder':'Site name'}),error_messages={'required':'Site Name is required'})
    description=forms.CharField(widget=forms.Textarea(attrs={'aria-label':'description','class':'form-control','placeholder':'Site Description'}),error_messages={'required':'Site Description is required'})
    theme_color=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'theme_color','class':'form-control gradient-colorpicker input-rounded','placeholder':'Site Theme Color eg #ff0000'}),required=False)
    key_words=forms.CharField(widget=forms.TextInput(attrs={'data-role':'tagsinput','aria-label':'key_words','class':'form-control input-rounded ','placeholder':'Site Keywords'}),required=False)
    site_url=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'site_url','class':'form-control input-rounded','placeholder':'Site URL'}),error_messages={'required':'Site URL is required'})
    favicon=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'favicon','class':'custom-file-input','id':'customFileInput','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','ico'],message="Invalid image extension",code="invalid_extension")]
                                )
    website_logo=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'website_logo','class':'custom-file-input','id':'customFileInput1','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','ico'],message="Invalid image extension",code="invalid_extension")]
                                ) 
    login_logo=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'login_logo','class':'custom-file-input','id':'customFileInput2','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','ico'],message="Invalid image extension",code="invalid_extension")]
                                )
    footer_logo=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'footer_logo','class':'custom-file-input','id':'customFileInput3','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','ico'],message="Invalid image extension",code="invalid_extension")]
                                )
    email_template_logo=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'email_template_logo','class':'custom-file-input','id':'customFileInput4','accept':'image/*','hidden':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','ico'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=SiteModel
        fields=['site_name','theme_color','site_url','description','key_words','favicon','website_logo','login_logo','footer_logo','email_template_logo',]
    
    def clean_theme_color(self):
        theme_color=self.cleaned_data['theme_color']
        match=re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$',theme_color)
        if not match:
            raise forms.ValidationError('Invalid color code given')
        else:
            return theme_color
            
    def clean_site_url(self):
        site_url=self.cleaned_data['site_url']
        if URLValidator(site_url):
            return site_url
        else:
            raise forms.ValidationError('Invalid url')

#AddressConfigForm
class AddressConfigForm(forms.ModelForm):
    site_email=forms.EmailField(widget=forms.EmailInput(attrs={'aria-label':'site_email','class':'form-control input-rounded','placeholder':'Site Email Address'}),error_messages={'required':'Address is required'})
    site_email2=forms.EmailField(widget=forms.EmailInput(attrs={'aria-label':'site_email2','class':'form-control input-rounded','placeholder':'Site Additional Email Address'}),required=False)
    address=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'address','class':'form-control input-rounded'}),error_messages={'required':'Address is required'})
    location=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'location','class':'form-control input-rounded'}),error_messages={'required':'Location is required'})
    phone=PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'aria-label':'phone','class':'form-control input-rounded'},initial='KE'),required=False)
    class Meta:
        model=SiteModel
        fields=['address','location','phone','site_email','site_email2']
    
    def clean_site_email(self):
        email=self.cleaned_data['site_email']
        if self.instance.site_email:
            if email != self.instance.site_email:
                if SiteModel.objects.filter(site_email=email).exists():
                    raise forms.ValidationError('A user with this email already exists.')
                try:
                    validate_email(email)
                except ValidationError as e:
                    raise forms.ValidationError('Invalid email address.')
                return email
            else:
               return email
        else:
            if SiteModel.objects.filter(site_email=email).exists():
                raise forms.ValidationError('A user with that email already exist')
            try:
                validate_email(email)
            except ValidationError as e:
                raise forms.ValidationError('Invalid email address')
            return email


#social form
class SiteSocialForm(forms.ModelForm):
    facebook=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'facebook','class':'form-control input-rounded','placeholder':'Facebook Link'}),required=False)    
    twitter=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'twitter','class':'form-control input-rounded','placeholder':'Twitter Link'}),required=False)    
    instagram=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'instagram','class':'form-control input-rounded','placeholder':'Instagram Link'}),required=False)    
    linkedin=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'linkedin','class':'form-control input-rounded','placeholder':'Linkedin Link'}),required=False)   
    youtube=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'youtube','class':'form-control input-rounded','placeholder':'Youtube Link'}),required=False)    
    whatsapp=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'whatsapp','class':'form-control input-rounded','placeholder':'Whats App'}),required=False)
    class Meta:
        model=SiteModel
        fields=['facebook','twitter','linkedin','instagram','youtube','whatsapp',]

    def clean_facebook(self):
        facebook=self.cleaned_data['facebook']
        if URLValidator(facebook):
                output=urlparse(facebook)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [facebook,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_twitter(self):
        twitter=self.cleaned_data['twitter']
        if URLValidator(twitter):
                output=urlparse(twitter)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [twitter,username]
        else:
            raise forms.ValidationError('Invalid url')
    

    def clean_instagram(self):
        instagram=self.cleaned_data['instagram']
        if URLValidator(instagram):
                output=urlparse(instagram)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [instagram,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_linkedin(self):
        linkedin=self.cleaned_data['linkedin']
        if URLValidator(linkedin):
                output=urlparse(linkedin)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Username parameter missing')
                else:
                    return [linkedin,username]
        else:
            raise forms.ValidationError('Invalid url')
    
    def clean_youtube(self):
        youtube=self.cleaned_data['youtube']
        if URLValidator(youtube):
                output=urlparse(youtube)
                username=output.path.strip('/')
                if not username:
                    raise forms.ValidationError('Channel id parameter missing')
                else:
                    return [youtube,username]
        else:
            raise forms.ValidationError('Invalid url')
    def clean_whatsapp(self):
        whatsapp=self.cleaned_data['whatsapp']
        if URLValidator(whatsapp):
            output=urlparse(whatsapp)
            username=output.path.strip('/')
            if not username:
                raise forms.ValidationError('username parameter missing')
            else:
                return [whatsapp,username]
        else:
            raise forms.ValidationError('Invalid url')

#WorkingConfigForm
class WorkingConfigForm(forms.ModelForm):
    working_days=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'working_days','class':'form-control input-rounded'}),error_messages={'required':'Working days is required'})
    working_hours=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'working_hours','class':'form-control input-rounded'}),error_messages={'required':'Working hours is required'})

    class Meta:
        model=SiteModel
        fields=['working_days','working_hours',]



class BillForm(forms.ModelForm):
    electricity_bill=forms.CharField(widget=forms.NumberInput(attrs={'aria-label':'electricity_bill','class':'form-control input-rounded'}))
    class Meta:
        model=SiteModel
        fields=['electricity_bill',]

class MeterForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'name','class':'form-control input-rounded'}))
    class Meta:
        model=MeterModel
        fields=['name',]
    def clean_name(self):
        name=self.cleaned_data['name']
        if self.instance.name:
            if name != self.instance.name:
                if MeterModel.objects.filter(name=name).exists():
                    raise forms.ValidationError('Meter already exists')
                else:
                    return name
            else:
                return name
        else:
            if MeterModel.objects.filter(name=name).exists():
                raise forms.ValidationError('Meter already exists')
            else:
                return name

class EquipmentForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'name','class':'form-control input-rounded'}))
    class Meta:
        model=EquipmentModel
        fields=['name',]
    def clean_name(self):
        name=self.cleaned_data['name']
        if self.instance.name:
            if name != self.instance.name:
                if EquipmentModel.objects.filter(name=name).exists():
                    raise forms.ValidationError('Equipment name already exists')
                else:
                    return name
            else:
                return name
        else:
            if EquipmentModel.objects.filter(name=name).exists():
                raise forms.ValidationError('Equipment name already exists')
            else:
                return name

class ReadingForm(forms.ModelForm):
    meter_name=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'meter_name','placeholder':'Meter name'}))
    meter_location=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'meter_location','placeholder':'Meter reading location'}))
    meter_reading=forms.CharField(widget=forms.NumberInput(attrs={'aria-label':'meter_reading','placeholder':'Meter reading'}))
    date=forms.DateField(widget=forms.DateInput(attrs={'type':'date','aria-label':'date','placeholder':'Date of meter reading'}))
    class Meta:
        model=ReadingModel
        fields=['meter_name','meter_location','meter_reading','date',]

month_opts=[
            ('January','January'),
            ('February','February'),
            ('March','March'),
            ('April','April'),
            ('May','May'),
            ('June','June'),
            ('July','July'),
            ('August','August'),
            ('October','October'),
            ('November','November'),
            ('December','December'),
]
class CostForm(forms.ModelForm):
    quantity=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','aria-label':'quantity','placeholder':'Quantity'}))
    rating=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','aria-label':'rating','placeholder':'Rating in KWh'}))
    year=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','aria-label':'year','placeholder':'Year'}))
    month=forms.ChoiceField(choices=month_opts,widget=forms.Select(attrs={'class':'form-control','aria-label':'month','placeholder':'Select Month'}))
    total_cost=forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','aria-label':'Total cost','placeholder':'Total cost'}))
    class Meta:
        model=CostModel
        fields=['quantity','year','month','total_cost','rating',]

    def clean_month(self):
        month=self.cleaned_data['month']
        if self.instance.month:
            if month != self.instance.month:
                if CostModel.objects.filter(month=month).exists():
                    raise forms.ValidationError('Month already exists')
                else:
                    return month
            else:
                return month
        else:
            if CostModel.objects.filter(month=month).exists():
                raise forms.ValidationError('Month already exists')
            else:
                return month

#HomeForm
class HomeForm(forms.ModelForm):
    h1=forms.CharField(widget=forms.TextInput(attrs={'aria-label':'h1','class':'form-control input-rounded'}),required=False)
    h1_text=forms.CharField(widget=forms.Textarea(attrs={'aria-label':'h1_text','class':'form-control'}),required=False)  
    image=forms.ImageField(
                                widget=forms.FileInput(attrs={'aria-label':'image','class':'dropify','data-default-file':True}),
                                required=False,
                                validators=[FileExtensionValidator(['jpg','jpeg','png','gif'],message="Invalid image extension",code="invalid_extension")]
                                )
    class Meta:
        model=AboutModel
        fields=['h1','h1_text','image',]