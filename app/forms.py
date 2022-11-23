from django import forms
from app.models import *
class Studentform(forms.ModelForm):
    class Meta:
        model=Students
        fields='__all__'
    def clean_name(self):
        name=self.cleaned_data.get('name')
        return name.upper()
    def clean_hall_ticket(self):
        return self.cleaned_data.get('hall_ticket').upper()
    def clean_rank(self):
        rank=self.cleaned_data.get('rank')
        for i in rank:
            if i.isalpha():
                raise forms.ValidationError('Enter valid Rank')
        return rank
    def clean_phone(self):
        no=self.cleaned_data.get('phone')
        for i in no:
            if i.isalpha() or len(no)<10:
                raise forms.ValidationError("Enter valid number")
        return no
    def clean_username(self):
        return self.cleaned_data.get('username').title()
    
class Appplyform(forms.ModelForm):
    class Meta:
        model=Apply
        fields='__all__'
class Instituteform(forms.ModelForm):
    class Meta:
        model=Institution
        fields='__all__'
    def clean_code(self):
        code=self.cleaned_data.get("code")
        return code.upper()
    def clean_name(self):
        code=self.cleaned_data.get("name")
        return code.upper()
    def clean_address(self):
        code=self.cleaned_data.get("address")
        return code.upper()
