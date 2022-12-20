from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields, widgets, ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe

from accounts.models import Profile



class SignupForm(UserCreationForm):

    MALE ='m'
    FEMALE = 'f'
    PROFILE_GENDER_CHOICES = [
    (MALE, "آقا"),
    (FEMALE, "خانم")
]



    bio = forms.CharField(label="bio", required=False)
    phone_number = forms.IntegerField(label="شماره تلفن همراه", help_text="11رقم وارد کنید", required=False)
    age = forms.CharField(max_length=2, label="سن", help_text="2رقم وارد کنید", required=False)
    job = forms.CharField(max_length=50, label="سمت شغلی", required=False)
    gender = forms.ChoiceField(label="جنسیت", choices=PROFILE_GENDER_CHOICES, required=False)
    nc = forms.CharField(label="کدملی", max_length=11, required=False) #nationalcode

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','email', 'bio', 'password1', 'password2']



class LoginForm(forms.Form):
    username = forms.CharField(label="username", label_suffix=":", widget=forms.TextInput(attrs={
        'class':"input100 calc__total-cost", "title":""
    }))
    password = forms.CharField(label="password", label_suffix=":", widget=forms.PasswordInput(attrs={
        'class': "input100 calc__total-cost", "title":""
    }))



class ProfileForm(forms.ModelForm):

    def limit_file_size(value):
        if value.size > 10485760:
            raise ValidationError("عکس عکس باید کمتر از 10 مگابایت باشد.")

    def persons_image_path(instance, filename):
        return 'persons/images/%s.%s' % (instance.first_name, filename.split(".")[-1])



    MALE ='m'
    FEMALE = 'f'
    PROFILE_GENDER_CHOICES = [
    (MALE, "آقا"),
    (FEMALE, "خانم")
]


    bio = forms.CharField(label="bio", required=False)
    phone_number = forms.IntegerField(label="شماره تلفن همراه", help_text="11رقم وارد کنید", required=False)
    age = forms.CharField(max_length=2, label="سن", help_text="2رقم وارد کنید", required=False)
    job = forms.CharField(max_length=50, label="سمت شغلی", required=False)
    gender = forms.ChoiceField(label="جنسیت", choices=PROFILE_GENDER_CHOICES, required=False)
    nc = forms.CharField(label="کدملی", max_length=11, required=False) #nationalcode
    #image = forms.ImageField(label="عکس",upload_to=persons_image_path, validators=[limit_file_size], required=False)
    class Meta:

        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            "username":"User Name",
            "first_name":"First Name",
            "last_name":" Last Name",
            "email":"Email"
        }
        help_texts = {
            'username':"Type in English",
            'first_name':"Type in English",
            'last_name':"Type in English",
            'email':"Type in English"
        }

        first_name = 'first_name'
        last_name = 'last_name'




    def clean_username(self):
        cleaned_data = self.clean()
        username = cleaned_data['username']

        if len(username) < 5:
            self.add_error('username', "username must be atleast more than 5 character")
        return username
    

    # by this we can make initial our form to dont be changable in profile admin
    """def __init__(self, *args, **kwargs):
       super(ProfileForm, self).__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['disabled'] = True"""

