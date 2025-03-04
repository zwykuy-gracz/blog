from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Tag


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False
    )

    class Meta:
        model = Post
        fields = ["title", "content", "published_date", "tags"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["published_date"].widget = forms.DateTimeInput(
                attrs={"type": "datetime-local"}
            )

    published_date = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label="Search")
