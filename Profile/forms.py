from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget

class CategoiesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ('name', 'desc')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',  'size':55, 'maxlength':50}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'name': 'ประเภทสินค้า',
            'desc': 'รายละเอียด',
        }
    def deleteForm(self):
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['desc'].widget.attrs['readonly'] = True


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('pid', 'name','detail', 'category', 'price', 'net', 'picture', )
        widgets = {
            'pid': forms.TextInput(attrs={'class': 'form-control',  'size':15, 'maxlength':10}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'size':55, 'maxlength':50}),
            'detail' : forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'Min': 1}),
            'net': forms.NumberInput(attrs={'class': 'form-control', 'Min': 0}),
            'picture':forms.FileInput(attrs={'class': 'form-control', 'accept':'image/*'}),
        }
        labels = {
            'pid': 'รหัสสินค้า',
            'name': 'ชื่อสินค้า',
            'detail': 'รายละเอียด',
            'category': 'ประเภทสินค้า',
            'price': 'ราคาต่อหน่วย',
            'net': 'คงเหลือ',
            'picture': 'ภาพสินค้า',
        }

    def updateForm(self):
        self.fields['pid'].widget.attrs['readonly'] = True
        self.fields['pid'].label = 'รหัสสินค้า [ไม่อนุญาตให้แก้ไขได้]'

    def deleteForm(self):
        self.fields['pid'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['category'].widget.attrs['readonly'] = True
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['net'].widget.attrs['readonly'] = True
        self.fields['picture'].widget.attrs['readonly'] = True

