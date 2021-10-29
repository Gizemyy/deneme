from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import Profile


class LoginForm(forms.Form):# bir modelden bağımsız form geliştirmek istiyorsak Modelform yerine form
    username = forms.CharField(max_length=50, label="kullanıcı adı")
    password = forms.CharField(max_length=50, label="parola", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Kullanıcı adını veya şifreyi yanlış girdiniz!")
        return super(LoginForm, self).clean()

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label='Kullanıcı Adı')
    password1 = forms.CharField(max_length=100, label='Parola', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, label='Parola Doğrulama', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifreler eşleşmiyor!")
        return password2


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'profile_pic',
            'birthday',
            'city',
        ]


