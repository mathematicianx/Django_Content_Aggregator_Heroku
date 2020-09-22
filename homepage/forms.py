from .models import SimpleAd, Profile, ForumTopic, ForumResponse
from django import forms
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

class SimpleAdForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label='Treść ogłoszenia')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SimpleAdForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SimpleAd
        fields = ('title', 'body', 'price', 'image',)
        labels = {
            'title': 'Tytuł',
            'price': 'Cena w zł',
            'image': 'Zdjęcie'
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        labels = {
            'username': 'Nazwa użytkownika',
            'first_name': 'Imię',
            'email': 'adres e-mail',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'adres e-mail',
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
        labels = {
            'date_of_birth': 'Data urodzenia',
            'photo': 'Miniaturka profilu',
        }


class CreateTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ('title', 'author', 'body')
        labels = {
            'title': 'Temat posta',
            'author': 'autor',
            'body': 'Treść posta',
        }


class CreateResponseForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label='Dodaj post')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateResponseForm, self).__init__(*args, **kwargs)


    class Meta:
        model = ForumResponse
        fields = ('body',)
        labels = {
            'body': 'Treść posta',
        }


