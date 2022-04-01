from django import forms
from .models import Comment, Like
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = ("text", "name", "email", "captcha")


class LikeForm(forms.ModelForm):
    like = forms.BooleanField(widget=forms.RadioSelect())

    class Meta:
        model = Like
        fields = ("like",)