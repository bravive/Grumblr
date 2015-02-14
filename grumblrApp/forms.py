from django import forms
from models import *
from forms import *
#from grumblrApp.forms import *
from django.contrib.auth.models import User
def my_errors(field):
    my_default_errors = {
        'required': '%s is required' % field,
        'invalid': 'Enter a valid value'
    }
    return my_default_errors
    
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ('owner', )
        widgets = {'picture' : forms.FileInput(),
                    'first_name' : forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control','style':'width:300px'}),
                    'last_name' : forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control','style':'width:300px'}),
                    'address_1' : forms.TextInput(attrs={'placeholder': 'Address_1','class': 'form-control','style':'width:300px'}),
                    'address_2' : forms.TextInput(attrs={'placeholder': 'Address_2','class': 'form-control','style':'width:300px'}),
                    'city' : forms.TextInput(attrs={'placeholder': 'City','class': 'form-control','style':'width:300px'}),
                    'state' : forms.TextInput(attrs={'placeholder': 'State','class': 'form-control','style':'width:300px'}),
                    'zip' : forms.TextInput(attrs={'placeholder': 'Zip','class': 'form-control','style':'width:300px'}),
                    'country' : forms.TextInput(attrs={'placeholder': 'Country','class': 'form-control','style':'width:300px'}),
                    'phone' : forms.TextInput(attrs={'placeholder': 'Phone','class': 'form-control','style':'width:300px'}),
                    }
        
class RelationshipForm(forms.ModelForm):
    class Meta:
        model=UserRelationship
        exclude = ('user','followings','blockings',)
        
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        exclude = ('item','user')
        widgets = {
                    'text': forms.TextInput(attrs={'placeholder': 'Reply...','class': 'form-control','style':'width:100px'}),
                    }
        
class ComposeForm(forms.ModelForm):
    class Meta:
        model=Grumbls
        exclude = ('user', 'dislike_user')
        widgets = {
                    'text': forms.TextInput(attrs={'placeholder': 'Composing...','class': 'form-control','style':'width:275px'}),
                    } 
                    
class SearchForm(forms.Form):
    search = forms.CharField(max_length=400,
                                widget=forms.TextInput(attrs={'placeholder': 'Search...','class': 'form-control','onkeydown':'if(event.keyCode==13){gosubmit();}'}))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control'})) 
    password = forms.CharField(max_length=200,
                                label='Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control'}))
class PasswordForm(forms.Form):
    password1 = forms.CharField(max_length=200,
                               label='New Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'New Password','class': 'form-control'}))
    password2 = forms.CharField(max_length=200,
                               label='New Password Again',
                               widget=forms.PasswordInput(attrs={'placeholder': 'New Password Again','class': 'form-control'}))
    def clean(self):
        #cleaned_data & clean is inherinted from parent
        cleaned_data = super(PasswordForm,self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1!= password2:
            raise forms.ValidationError("Password did not match.")
        return cleaned_data

class ResetForm(forms.Form):
    email = forms.EmailField(max_length=200,
                             widget=forms.TextInput(attrs={'placeholder': 'Conformation Email','class': 'form-control','style': 'width:383px'}),
                             error_messages=my_errors('Email'))

class RegistrationForm(forms.Form):
    
    firstname = forms.CharField(max_length=200,
                                widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'form-control'}),
                                error_messages=my_errors('First Name'))
    lastname = forms.CharField(max_length=200,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'form-control'}),
                                error_messages=my_errors('Last Name')) 
    email = forms.EmailField(max_length=200,
                                widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'form-control','style': 'width:383px'}),
                                error_messages=my_errors('Email'))
    username = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-control','style': 'width:383px'}),
                                error_messages=my_errors('Username')) 
    password1 = forms.CharField(max_length=200,
                                label='Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control','style': 'width:383px'}),
                                error_messages=my_errors('Password'))
    password2 = forms.CharField(max_length=200,
                                label='Conform Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Conform Password','class': 'form-control','style': 'width:383px'}),
                                error_messages=my_errors('Conform Password'))     
    def clean(self):
        #cleaned_data & clean is inherinted from parent
        cleaned_data = super(RegistrationForm,self).clean()
        
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1!= password2:
            raise forms.ValidationError("Password did not match.")
            
        return cleaned_data
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.")
        return email
    def clean_username(self):
        username=self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username