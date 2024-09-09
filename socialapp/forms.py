from django import forms
from .models import User, Profile, Post
from django.contrib.auth.forms import UserCreationForm


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email', 'required':'true'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'password1',
        })
        self.fields["password2"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'password2',
        })

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profilepic', 'wallpaper', 'bio', 'address', 'dateofbirth', 'gender', 'marital']
        labels = {
            'profilepic': 'Profile Picture',
            'profilepic': 'Profile Wallpaper',
            'dateofbirth':'Date Of Birth',
            'marital': 'Marital Status',
        }
        widgets = {
            'bio': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Bio'}), 
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
            'dateofbirth': forms.DateInput(attrs={'class':'form-control', 'type':'date'}), 
            'gender': forms.Select(attrs={'class':'form-control'}),
            'marital': forms.Select(attrs={'class':'form-control'}), 
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption',]
        widgets = {
            'caption': forms.Textarea(attrs={'class':'form-control', 'placeholder':'What is on your mind...'}), 
        }