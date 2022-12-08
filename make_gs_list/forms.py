from django import forms
from .models import GoodsService

class InForm(forms.Form):
    input = forms.CharField(label='商品役務表記を入力してください', \
        widget = forms.Textarea(attrs={'class':'form-control'}))

# class GSForm(forms.ModelForm):
#     cls = forms.CharField(label='区分')
#     jpn = forms.CharField(label='商品役務（日本語）')
#     eng = forms.CharField(label='商品役務（英語）')
#     ruijigun = forms.CharField(label='類似群')
#     nice = forms.CharField(label='ニース固有番号')
#     kijun_flg = forms.BooleanField(label='商品役務基準')
#     nice_flg = forms.BooleanField(label='ニース分類')

# class HiddenForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         cls = forms.CharField(initial="", widget=forms.HiddenInput)
#         jpn = forms.CharField(initial="", widget=forms.HiddenInput)
#         eng = forms.CharField(initial="", widget=forms.HiddenInput)
#         ruijigun = forms.CharField(initial="", widget=forms.HiddenInput)
#         nice = forms.CharField(initial="", widget=forms.HiddenInput)