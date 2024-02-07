from django import forms
#from .models import EstimateInfo

class InForm(forms.Form):
    cname = forms.CharField(label='クライアント名', \
        widget = forms.TextInput(attrs={'class':'form-control'}))
    mark = forms.CharField(label='商標', \
        widget = forms.TextInput(attrs={'class':'form-control'}))
    kubun = forms.CharField(label='区分', \
        widget = forms.TextInput(attrs={'class':'form-control'}))
    mitsumori_num = forms.CharField(label='見積番号', \
        widget = forms.TextInput(attrs={'class':'form-control'}))
    discount = forms.IntegerField(label='割引', min_value=0, max_value=100, \
        widget = forms.NumberInput(attrs={'class':'form-control'}))

    #input = forms.CharField(label='見積情報を入力してください', \
    #    widget = forms.Textarea(attrs={'class':'form-control'}))
