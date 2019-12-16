from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate
from .models import *
from django_summernote.widgets import SummernoteWidget
from django_select2.forms import Select2MultipleWidget


Boolean_Choice = [
    ('1', 'Yes'),
    ('0', 'No'),
]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'username(email)',
                   'style': 'padding-left:5px;'
                   }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'style': 'padding-left:5px;'
            }))


class SignUpForm(forms.ModelForm):

    class Meta:
        model = NewUser
        fields = ('first_name', 'last_name', 'email')

        widgets = {
            'groups': forms.SelectMultiple(attrs={

                'style': 'width:250px;height:40px;',
                'required': 'True'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_email(self):
        data = self.cleaned_data['email']

        if not data:
            raise forms.ValidationError("email cannot be Empty")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')


class NewPassword(forms.Form):
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput)


class DesignationForm(forms.ModelForm):

    class Meta:
        model = Designation
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
                'required': 'True'}),
        }


'''Post part '''


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # populates the post
        self.fields['category'].queryset = Category.objects.filter(
            deleted_at__isnull=True)
        # self.fields['subcategory'].queryset = SubCategory.objects.filter(deleted_at__isnull=True)

    class Meta:
        model = Post

        fields = ['title', 'category', 'subcategory', 'author', 'slug', 'description', 'content',
                  'photo', 'photo_caption','publish']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type Post Title',
                'required': 'True',
                'style': 'border:1px #D5D5D5 solid; padding-left:5px;'
            }),

            'photo_caption': forms.TextInput(attrs={
                'class': 'form-control',

                'placeholder': 'Type Photo Caption',
                'style': 'border:1px #D5D5D5 solid; padding-left:5px;'
            }),

            'content': SummernoteWidget(attrs={
                'width': '600px',
                'height': '200px'
            }),
            'description': forms.Textarea(attrs={
                'class': 'descriptionfield',
            }),

            'subcategory': Select2MultipleWidget(attrs={
                'class': 'form-control borderline'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control borderline',
            }),

            'author': forms.Select(attrs={
                'class': 'form-control borderline',
                'placeholder': 'Name'}),

            'photo': forms.FileInput(attrs={
                'class': '',
            }),

            'slug': forms.TextInput(attrs={
                'class': 'form-control '
            }
            )

        }


class PostDraftForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = ['publish']
        widgets = {
            'publish': forms.RadioSelect(choices=Boolean_Choice),
        }


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ['name', 'description', 'photo', 'priority']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of author',
                'required': 'True',
                'style': 'border:1px #D5D5D5 solid; padding-left:5px;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'descriptionfield',
            }),
        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'parent', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
                'required': 'True',
                'style': 'border:1px #D5D5D5 solid; padding-left:5px;'
            }),

        }


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ['title', 'parent', 'position', 'urls']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type Post Title',
                'required': 'True',
                'style': 'border:1px #D5D5D5 solid; padding-left:5px;'
            }),
            'parent': forms.Select(attrs={
                'class': 'form-control borderline',

            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border:1px #D5D5D5 solid;max-width:250px; padding-left:5px;'
            }),
            'urls': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border:1px #D5D5D5 solid; max-width:250px; padding-left:5px;'
            }),
        }


class FormMenu(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ['title', 'parent', 'position', 'urls']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control borderline',
                'style': 'padding-left:5px;'
            }),
            'parent': forms.Select(attrs={
                'class': 'form-control borderline',
            }),
            'urls': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border:1px #D5D5D5 solid; max-width:350px; padding-left:5px;'
            }),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class AdvertisementForm(forms.ModelForm):

    class Meta:
        model = Advertisement

        fields = ['title', 'place1', 'place2', 'ad_type',
                  'embedded_code', 'url', 'is_enabled', 'priority', 'expired_at']

        widgets = {
            'expired_at': DateInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border:1px #D5D5D5 solid; padding-left:5px;'
            }),
            'ad_type': forms.Select(attrs={
                'class': 'form-control borderline',
                'style': 'max-width:200px;'
            }),
            'embedded_code': forms.Textarea(attrs={
                'class': 'descriptionfield',
            }),
            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'border:1px #D5D5D5 solid; padding-left:5px;'
            }),

            'is_enabled': forms.RadioSelect(choices=Boolean_Choice),

        }
