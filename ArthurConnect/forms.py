from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import ContactMessage, Review

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'username',
            'email',
            'password1',
            'password2',
            Submit('submit', 'S\'inscrire', css_class='btn btn-primary')
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Se connecter', css_class='btn btn-primary')
        )

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'subject',
            'message',
            Submit('submit', 'Envoyer le message', css_class='btn btn-primary')
        )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} étoile{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'rating',
            'title',
            'comment',
            Submit('submit', 'Publier l\'avis', css_class='btn btn-primary')
        )

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Rechercher des formations...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    price_min = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Prix min',
            'class': 'form-control'
        })
    )
    price_max = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Prix max',
            'class': 'form-control'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
