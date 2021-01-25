from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'username',
                  'password']
        # excludes = ['']
        
        label = {
            'password': 'Password'
        }

    def save(self):
        password = self.cleaned_data.pop('password')
        u = super().save()

        u.set_password(password)
        u.save()
        return u

class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']