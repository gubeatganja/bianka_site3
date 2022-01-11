from django import forms
from .models import Comment
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = ("text", "name", "email", "captcha")
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control border"}),
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
        }
