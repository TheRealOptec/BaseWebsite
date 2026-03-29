from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from mybase.models import Comment, Topic, UserProfile


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your username",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
            }
        ),
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Choose a username",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
            }
        ),
    )
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Create a password",
            }
        ),
    )
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Repeat your password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserAccountForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        strip=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        ),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email address",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        return self.cleaned_data["username"].strip()


class UserProfileEditForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Write something about yourself...",
            }
        ),
    )
    pfp = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "accept": "image/*",
            }
        ),
    )

    class Meta:
        model = UserProfile
        fields = ("pfp", "bio")


class TopicForm(forms.ModelForm):
    name = forms.CharField(
        max_length=60,
        strip=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. Film Recommendations",
                "maxlength": 60,
            }
        ),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "maxlength": 500,
                "placeholder": "Explain what this topic is for and what people should post here.",
            }
        ),
    )

    class Meta:
        model = Topic
        fields = ("name", "description")

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Topic name cannot be blank.")
        return name


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        max_length=320,
        strip=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Write your comment here...",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ("body",)

    def clean_body(self):
        body = self.cleaned_data["body"].strip()
        if not body:
            raise forms.ValidationError("Comment cannot be blank.")
        return body


class PostForm(forms.Form):
    title = forms.CharField(
        max_length=60,
        strip=False,
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
