from django import forms
#from .models import EstimateInfo

class InForm(forms.Form):
    cname = forms.CharField(label='クライアント名')
    mark = forms.CharField(label='商標')
    kubun = forms.CharField(label='区分')
    mitsumori_num = forms.CharField(label='見積番号')
    discount = forms.IntegerField(label='割引', min_value=0, max_value=100)
    countries = forms.CharField(label='国名')

    #input = forms.CharField(label='見積情報を入力してください', \
    #    widget = forms.Textarea(attrs={'class':'form-control'}))
