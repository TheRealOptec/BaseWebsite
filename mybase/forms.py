from django import forms
from django.contrib.auth.models import User
from mybase.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('pfp',)


class PostForm(forms.Form):
    title = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your post title",
            }
        ),
    )
    body = forms.CharField(
        max_length=500,
        strip=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control simplesEditor simplesin-main",
                "rows": 8,
                "placeholder": "Write your post here...",
            }
        ),
    )

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Title cannot be blank.")
        return title

    def clean_body(self):
        body = self.cleaned_data["body"]
        if not body.strip():
            raise forms.ValidationError("Post content cannot be blank.")
        return body
